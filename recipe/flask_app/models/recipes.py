from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Recipes:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.description= data['description']
        self.date = data['date']
        self.time= data['time']
        self.instructions= data['instructions']
        self.id_recipe = data['id_recipe']
      

    @classmethod
    def get_all_recipes (cls):
        query = "SELECT  user.id , recipes.id as id_recipe , user.first_name ,user.last_name ,recipes.description,recipes.date, recipes.time, recipes.instructions FROM user  JOIN recipes ON recipes.user_id = user.id;"
        # los nombres deben ser los de la bd / los valores los del html
        results = connectToMySQL('recipes').query_db(query)
        print(results)
        recipes = []
        # crea arreglo para guiardar los valores 
        for recipe in results: #itera los nombres de la base de datos 
            data = {
                "id" : recipe["id"],
                "first_name" : recipe["first_name"],
                "last_name" : recipe["last_name"],
                "description" : recipe["description"],
                "date" : recipe["date"],
                "time" : recipe["time"],
                "instructions" : recipe["instructions"],
                "id_recipe" : recipe["id_recipe"]
                }
            recipes.append(cls(recipe))
        
            # flos mete en el arreglo -y los convierte en una clkase ususario
        return recipes


    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if  len(data['name']) < 3:
            flash("Name must be at least characters .")
            is_valid = False
        if  len(data['description']) < 3:
            flash("Description must be at least characters .")
            is_valid = False
        if  len(data['instructions']) < 3:
            flash("Instructions must be at least characters .")
            is_valid = False
        return is_valid
        

    @classmethod
    def save(cls, data):
        query = "INSERT INTO  recipes (name, description, time, instructions,date, created_at, updates_at, user_id) VALUES ( %(name)s , %(description)s , %(time)s , %(instructions)s , %(date)s , NOW() , NOW(),%(user_id)s);"
        # los nombres deben ser los de la bd / los valores los del html
        new_recipe_id= connectToMySQL('recipes').query_db(query, data)
        return 

  