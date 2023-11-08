from flask_app.config.mysqlconnection import connectToMySQL

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email= data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"

        results = connectToMySQL('usersHw').query_db(query)
        # guarda el resultado de la bd
        
        users = []
        # crea arreglo para guiardar los valores 
        for user in results: #itera los nombres de la base de datos 
            users.append(cls(user))
            # flos mete en el arreglo -y los convierte en una clkase ususario
        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users ( first_name , last_name , email , created_at, updated_at ) VALUES ( %(uname)s , %(ulastname)s , %(uemail)s , NOW() , NOW() );"
        # los nombres deben ser los de la bd / los valores los del html
        return connectToMySQL('usersHw').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s"
        connectToMySQL('usersHw').query_db(query, data)
        return 

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        # los nombres deben ser los de la bd / los valores los del html
        result= connectToMySQL('usersHw').query_db(query, data)
        single_user= cls(result[0]) 
        return single_user

    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(uname)s , last_name = %(ulastname)s , email= %(uemail)s , created_at = NOW(), updated_at= NOW() WHERE id= %(id)s;"
        # los nombres deben ser los de la bd / los valores los del html
        return connectToMySQL('usersHw').query_db(query, data)


