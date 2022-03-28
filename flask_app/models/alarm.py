from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

import datetime
import time
from playsound import playsound

class Alarm:
    db = 'alarms'
    def __init__( self , data ):
        self.id = data['id']
        self.alarm_name = data['alarm_name']
        self.hour = data['hour']
        self.minute = data['minute']
        self.ampm = data['ampm']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    def check_alarm_input(alarm_time):
        """Checks to see if the user has entered in a valid alarm time"""
        if len(alarm_time) == 1: # [Hour] Format e xample only typing 22
            if alarm_time[0] < 24 and alarm_time[0] >= 0: # under 24 because at midnight 12am because 0
                return True
        if len(alarm_time) == 2: # [Hour:Minute] Format example only typing 22:01
            if alarm_time[0] < 24 and alarm_time[0] >= 0 and \
                alarm_time[1] < 60 and alarm_time[1] >= 0: # under 60 because at new hour 60 becomes 0
                return True
        elif len(alarm_time) == 3: # [Hour:Minute:Second] Format example typing in 22:01:30
            if alarm_time[0] < 24 and alarm_time[0] >= 0 and \
                alarm_time[1] < 60 and alarm_time[1] >= 0 and \
                alarm_time[2] < 60 and alarm_time[2] >= 0: # under 60 because at new minute 60 becomes 0
                return True
        return False
    # Get user input for the alarm time
    # print("Set a time for the alarm (Ex. 06:30 or 18:30:00)")
    def alarm(data):
        while True:
            alarm_input = f"{data['hour']}:{data['minute']}"
            print(alarm_input)
            try:
                alarm_time = [int(n) for n in alarm_input.split(":")]
                if check_alarm_input(alarm_time):
                    if(data['ampm'] == 'pm'):
                        alarm_time[0] = alarm_time[0] + 12
                # print(alarm_time) ths is just for me. but this print would show what alarm_time looks like. 10:01 would be [10, 01]
                    break
                else:
                    raise ValueError
            except ValueError:
                print("ERROR: Enter time in HH:MM or HH:MM:SS format")
        #Convert the alarm time from [H:M] or [H:M:S] to seconds
        seconds_hms = [3600, 60, 1] # Number of seconds in an Hour, Minute, and Second
        alarm_seconds = sum([a*b for a,b in zip(seconds_hms[:len(alarm_time)], alarm_time)]) #gives how many seconds in the time inputted for example 1am is 3600 seconds
        #print(alarm_seconds) just for me. printed version of above looks like
        # Get the current time of day in seconds
        now = datetime.datetime.now()
        current_time_seconds = sum([a*b for a,b in zip(seconds_hms, [now.hour, now.minute, now.second])])#gives how many seconds at current time of day
        # Calculate the number of seconds until alarm goes off
        time_diff_seconds = alarm_seconds - current_time_seconds
        # If time difference is negative, set alarm for next day
        if time_diff_seconds < 0:
            time_diff_seconds += 86400 # number of seconds in a day
        # Display the amount of time until the alarm goes off
        print("Alarm set to go off in %s" % datetime.timedelta(seconds=time_diff_seconds)) #puts seconds in time difference to 00:00:00
        # Sleep until the alarm goes off
        time.sleep(time_diff_seconds)
        # Time for the alarm to go off
        print("Wake Up!")
        playsound(r"C:/Users/danie/OneDrive/Documents/python/flask_mysql/alarms/flask_app/static/sound/alarm.mp3")


    @classmethod
    def save(cls, data ):
        query = "INSERT INTO alarms (alarm_name, hour, minute, ampm, user_id) " \
        "VALUES ( %(alarm_name)s, %(hour)s, %(minute)s, %(ampm)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod 
    def get_all_with_user(cls, data):
        query = "SELECT * FROM alarms LEFT JOIN users on alarms.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        alarms = []
        if results:
            for row in results:
                # print(row)
                this_alarm = cls(row)
                user_data = {
                    **row,
                    "users.id": row["users.id"],
                    "created_at": row["users.created_at"],
                    "updated_at": row["users.updated_at"]
                }
                this_alarm.user = user.User(user_data) #what ever comes after this_painting neeeds to be called in html when wanting user data. does not need to be named user. can be named anything like "bro", html just needs to be the same too 
                alarms.append(this_alarm)
        return alarms

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM alarms WHERE alarms.id= %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_one_alarm_with_user(cls, data ): #use this for one to one
        query = "SELECT * FROM alarms LEFT JOIN users on alarms.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        # print(results)
        if results:
            row = results[0]
            one_alarm = cls(row) # or cls(results[0])
            #need to make a data dictionary for the associated class
            user_data = {
                **row,
                "id": row["users.id"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
            one_alarm.user = user.User(user_data)
        return one_alarm

    @classmethod
    def update(cls, data ):
        query = "UPDATE alarms SET alarm_name = %(alarm_name)s, hour = %(hour)s, minute = %(minute)s, ampm = %(ampm)s" \
        "WHERE id = %(id)s;"
        print(query)
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM alarms WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def alarm_valid(data):
        is_valid = True
        # try:
        #     val = int(float(data['hour']))
        # except ValueError:
        #     flash("Do not use letters for hour and minutes!", "create")
        hour = data['hour']
        minute = data['minute']
        if len(data['alarm_name']) < 3:
            is_valid = False
            flash("Alarm name must be at least 3 character", "create")
        if not hour.isdigit():
            is_valid = False
            flash("Hour cannot be a letter and must be between 1-12", "create")
        elif data['hour'] == '' or int(float(data['hour'])) > 12 or int(float(data['hour'])) < 1:
            is_valid = False
            flash("Hour must be between 1-12", "create")
        if not minute.isdigit():
            is_valid = False
            flash("Minute cannot be a letter and must be between 0 and 60", "create")
        elif data['minute'] == '' or int(float(data['minute'])) > 60 or int(float(data['minute'])) < 0:
            is_valid = False
            flash("Minute must be between 0 and 60", "create")
        elif len(data['minute']) < 2:
            is_valid = False
            flash("Minute must be in MM format", "create")
        if data['ampm'] == '':
            is_valid = False
            flash("Must choose am or pm", "create")
        return is_valid