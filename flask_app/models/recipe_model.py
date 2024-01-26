from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB
from flask_app.models import user_model
import re



class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under30 = data['under30']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO recipes (name, description, instructions, under30, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(under30)s, %(user_id)s)"  
        results = connectToMySQL(DB).query_db(query, data)
        
        return results
    
    @classmethod
    def get_recipes_users(cls):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id"
        results = connectToMySQL(DB).query_db(query)

# this weird stuff here just creates class instances for all of the data. If you don't do this the SELECT just returns a list of dictionaries
# and you won't be able to use class methods on them
        recipe_row = []
        for row in results:
            new_recipe = cls(row)

            creator_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at']
                }
            new_recipe.creator = user_model.User(creator_data)


            recipe_row.append(new_recipe)
        
        return recipe_row
    


    @classmethod
    def get_one(cls, id):
        data = {
        "id":id
        }

        query = """
            SELECT * FROM recipes WHERE id = %(id)s
        """
        results = connectToMySQL(DB).query_db(query, data)

        if results:
            row = results[0]
            new_recipe = cls(row)
            return new_recipe
        
    @classmethod
    def update(cls, data):

        query = """
            UPDATE recipes 
            SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under30 = %(under30)s
            WHERE id = %(id)s
        """
        connectToMySQL(DB).query_db(query, data)

    @classmethod
    def delete(cls, id):
        data = {
            "id":id
        }

        query = """
            DELETE FROM recipes WHERE id = %(id)s
        """
        return connectToMySQL(DB).query_db(query, data)