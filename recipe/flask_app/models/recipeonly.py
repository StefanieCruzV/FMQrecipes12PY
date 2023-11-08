from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Recipes_only:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.time= data['time']
        self.instructions = data['instructions']
        self.date= data['date']
        self.created_at= data['created_at']
        self.updates_at = data['updates_at']
        self.user_id = data['user_id']
      
    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        # los nombres deben ser los de la bd / los valores los del html
        result= connectToMySQL('recipes').query_db(query, data)
        print(result)
        single_recipe= cls(result[0]) 
        print(single_recipe)
        return single_recipe
    
    @classmethod
    def update_recipe_by_id(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, time= %(time)s, instructions = %(instructions)s,date= %(date)s, updates_at = now() WHERE id = %(id)s"
        # los nombres deben ser los de la bd / los valores los del html
        return   connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def dele_recipe_by_id(cls, data):
        query = "DELETE FROM recipes WHERE id= %(id)s"
        # los nombres deben ser los de la bd / los valores los del html
        return  connectToMySQL('recipes').query_db(query, data)