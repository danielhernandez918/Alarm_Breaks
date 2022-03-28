from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask import flash


class User:
    db = 'alarms'
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users (first_name, last_name, email, password) " \
        "VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        users = []
        results = connectToMySQL(cls.db).query_db(query)
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def update(cls, data ):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s" \
        "WHERE id = %(id)s;"
        print(query)
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update_password(cls, data ):
        query = "UPDATE users SET password = %(password)s" \
        "WHERE id = %(id)s;"
        print(query)
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def register_valid(data):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('belt').query_db(query,data)
        if len(results) >= 1:
            is_valid = False
            flash("Email already taken", "register")
        if not EMAIL_REGEX.match(data['email']):
            is_valid= False
            flash("Not a valid email", "register")
        if data['password'] != data['confirm_password'] :
            is_valid = False
            flash("Passwords don't match", "register")
        if len(data['first_name']) < 2:
            is_valid = False
            flash("First Name must be at least 3 characters", "register")
        if len(data['last_name']) < 2:
            is_valid = False
            flash("Last Name must be at least 3 characters", "register")
        if len(data['email']) < 7:
            is_valid = False
            flash("Email must be at least 7 characters", "register")
        if len(data['password']) < 8:
            is_valid = False
            flash("Password must be at least 8 characters", "register")
        return is_valid

    @staticmethod
    def account_update_valid(data):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('belt').query_db(query,data)
        if len(results) >= 2:
            is_valid = False
            flash("Email already taken", "register")
        if not EMAIL_REGEX.match(data['email']):
            is_valid= False
            flash("Not a valid email", "register")
        if len(data['first_name']) < 2:
            is_valid = False
            flash("First Name must be at least 2 characters", "update")
        if len(data['last_name']) < 2:
            is_valid = False
            flash("Last Name must be at least 2 characters", "update")
        if len(data['email']) < 7:
            is_valid = False
            flash("Email must be at least 7 characters", "register")
        return is_valid

    @staticmethod
    def password_update_valid(data):
        is_valid = True
        if data['password'] == data['current_password'] :
            is_valid = False
            flash("New and old passwords cant macth", "password")
        if len(data['password']) < 8:
            is_valid = False
            flash("Password must be at least 8 characters", "password")
        return is_valid

    # @classmethod
    # def delete(cls,data):
    #     query = "DELETE FROM users WHERE id = %(id)s;"
    #     return connectToMySQL(cls.db).query_db(query,data)