from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB
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
    def getbyemail(cls,data):
        query = 'SELECT * FROM users WHERE email = %(email)s'
        results = connectToMySQL(DB).query_db(query,data)
        
        if not results:
            return None
        
        return User(results[0])
    
    @classmethod
    def get_by_id(cls,id):
        query = 'SELECT * FROM users WHERE id = %(id)s'
        results = connectToMySQL(DB).query_db(query,{"id" : id})
        
        if not results:
            return None
        
        return User(results[0])
        
    # this is the method to create a user into our database

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"  
        results = connectToMySQL(DB).query_db(query, data)
        
        return results
    # create validation method

    @staticmethod
    def validate_user(user):
        is_valid = True
        
        if len(user['first_name']) < 3:
                flash("First Name must be at least 3 characters.", "registration")
                is_valid = False
        if len(user['last_name']) < 3:
                flash("Last Name must be at least 3 characters.", "registration")
                is_valid = False
                
        if len(user['email']) < 3:
                flash("Email must be at least 3 characters.", "registration")
                is_valid = False
        
    #checks email with regex
        if not EMAIL_REGEX.match(user['email']): 
                flash("Please enter a valid email.", "registration")
                is_valid = False
                
    #checks database for email
        if (re.fullmatch(EMAIL_REGEX, user['email'])):
            this_user = {
            'email': user['email']
            }
            results = User.check_database(this_user)
            if len(results) != 0:
                flash('An account already exists with that email; please login', "registration")
                is_valid = False
                
                
    #checks password
        if len(user['password']) < 3:
            flash("Password must be at least 3 characters.", "registration")
            is_valid = False
    #password has at least one number
        if(re.search('[0-9]', user['password']) == None ):
            flash("Password must include a number", "registration")
            is_valid = False
                
    #password has an upper case letter          
        if(re.search('[A-Z]', user['password']) == None ):
            flash("Password must include an upper case letter", "registration")
            is_valid = False
                
        
        
    #password and confirm password must match          
        if (user['password'] != user['password_confirmation']):
                flash("Passwords do not match!", "registration")
                
        return is_valid
    
    @staticmethod
    def validate_login(user):
        is_valid = True
        if len(user['email']) < 3:
                flash("Email must be at least 3 characters.", "login")
                is_valid = False
                
        if len(user['password']) < 3:
                flash("Password must be at least 3 characters.", "login")
                is_valid = False
                
    @classmethod
    def check_database(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        
        results = connectToMySQL(DB).query_db(query, data)
        
        return results
        
    #Read One User from Database
    
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        result = connectToMySQL(DB).query_db(query,data)
        return cls(result[0])


