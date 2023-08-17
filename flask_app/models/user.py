from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import item
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    DB = 'exam_prep'
    def __init__(self,data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    @classmethod
    def save(cls,data):
        query="""
        INSERT INTO users(first_name, last_name, email, password) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s,%(password)s);
        """
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_user(user):
        is_valid = True
        # test whether a field matches the pattern
        if len(user["first_name"])==0:
            flash("First Name must not be blank!")
            is_valid = False
        if len(user["last_name"])==0:
            flash("Last Name must not be blank!")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(user["password"])<8:
            flash("Password must be at least 8 characters!")
            is_valid = False

        return is_valid
    