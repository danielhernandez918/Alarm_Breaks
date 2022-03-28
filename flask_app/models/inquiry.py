from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Inquiry:
    db = 'alarms'
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.content = data['content']

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO inquiries (user_id, content) " \
        "VALUES ( %(user_id)s, %(content)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def contacted_valid(data):
        is_valid = True
        if len(data['content']) < 3:
            is_valid = False
            flash("Question or inquiry name must be at least 3 characters", "inquiry")
        return is_valid