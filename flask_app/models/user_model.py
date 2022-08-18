from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_one(cls, data):
        query = "SELECT * "
        query += "FROM users "
        query += "WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result)>0:
            return cls(result[0])
        else:
            return None
    
    @classmethod
    def get_one_id(cls, data):
        query= "SELECT * "
        query += "FROM users "
        query +="WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, password) "
        query += "VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @staticmethod
    def validate_session():
        if "user_id" in session:
            return True
        else:
            flash("You must be logged in.", "error_login")
            return False


    @staticmethod
    def validate_registration(data):
        isValid = True
        if data['first_name'] == "":
            flash("You must provide your first name.", "error_first_name_registration")
            isValid = False
        if data['last_name'] == "":
            flash("You must provide your last name.", "error_last_name_registration")
            isValid = False
        if data['email'] == "":
            flash("You must provide your email.", "error_email_registration")
            isValid = False
        if data['password'] == "":
            flash("You must provide a password.", "error_password_registration")
            isValid = False
        if data['confirm_password'] != data['password']:
            flash("Your password confirmation does not match.", "error_password_confirmation")
            isValid = False
        if len(data["first_name"]) < 2:
            flash("Your first name must be atleast 3 charecters long", "error_first_name_registration")
            isValid = False
        if len(data["last_name"]) < 2:
            flash("Your last name must be atleast 3 charecters long", "error_last_name_registration")
            isValid = False
        if len(data["password"]) < 8:
            flash("Your password must be atleast 8 charecters long.", "error_password_registration")
            isValid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Please provide a valid email", "error_email_registration")
            isValid = False
        return isValid

    @staticmethod
    def validate_login(data):
        isValid = True
        if data['email'] == "":
            flash("Please provide your email.", "error_email_login")
            isValid = False
        if data['password'] == "":
            flash("Please provide your password", "error_password_login")
            isValid = False
        return isValid