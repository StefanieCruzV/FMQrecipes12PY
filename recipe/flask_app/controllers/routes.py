from cgi import print_form
from crypt import methods
import re
from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models.user import User
from flask_app.models.recipes import Recipes
from flask_app.models.recipeonly import Recipes_only
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash

@app.route("/")
def index():
    return render_template("login.html") 

@app.route("/register", methods=["POST"])
def register():   
    if not User.validate_user(request.form): # is la validacion es falso mandamos a index
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password']) # crear Hash del password
    print(pw_hash)

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    } 
    # print(request.form)
    this_user = User.find_the_email(data)
    if  this_user: # if the query return  o == falrse
        flash("email is already use!")
        return redirect("/")


    use_id= User.save(data)
    session['logged_id'] = use_id
    return redirect("/success")


@app.route("/success")
def success():
    if"logged_id" not in session:
        return redirect("/")
    data ={
        "id" : session['logged_id']
    }
    loged_user= User.user_by_id(data)

    recipes = Recipes.get_all_recipes()


    # return f"you are logged in as user # {session['logged_id']} !"
    return render_template("recipeshare.html",loged_user=loged_user,recipes=recipes) 


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

#----------------------------------------------------registration


@app.route('/login', methods=["POST"])
def login():
    data ={
        "email" : request.form["email"]
    }
    this_user = User.find_the_email(data)
    if not this_user: # if the query return  o == falrse
        flash("invalid email/password")
        return redirect("/")
    #if user exist
    if not bcrypt.check_password_hash(this_user.password, request.form['password']):
        flash("password is wrong")
        return redirect("/")
    #-chec and cpompare the password

    session['logged_id']= this_user.id
 
    return redirect("/success")

#----------------------------------------------------loggin

@app.route('/create')
def create():
    if"logged_id" not in session:
        return redirect("/")

    return render_template("addrecipe.html") 


@app.route('/create_recipe', methods=["POST"])
def create_recipe():
    print(request.form)
    data = {
    "name": request.form["name"],
    "description": request.form["description"],
    "time": request.form["flexRadioDefault"],
    "date": request.form["date"],
    "instructions": request.form["instructions"],
    "user_id":  session['logged_id']
    }
    # print(data)
    recipes = Recipes.validate_recipe(data)
    this_recipe = Recipes.save(data)
 
    return redirect('/success')
#----------------------------------------------------CREATE

@app.route('/update_recipe/<int:id>')
def update_recipe(id):
    if"logged_id" not in session:
        return redirect("/")
   
    data = {
        "id": id,
        }
    recipe = Recipes_only.get_recipe_by_id(data)
    # print(recipe.name)
    return render_template("editrecipe.html",recipe=recipe) 


@app.route('/send_update_recipe', methods=["POST"])
def send_update_recipe():
    if"logged_id" not in session:
        return redirect("/")
    print(request.form)
    data = {
        "id":request.form["recipe_id"],
        "name": request.form["name"],
        "description": request.form["description"],
        "date": request.form["date"],
        "time": request.form["flexRadioDefault"],
        "instructions": request.form["instructions"]
    }
    Recipes_only.update_recipe_by_id(data)
    return redirect('/success')


@app.route('/delete_recipe/<int:id>')
def delete_user(id):
    if"logged_id" not in session:
        return redirect("/")
    print(id)
    data = {
        "id": id
        }
    Recipes_only.dele_recipe_by_id(data)
    return redirect('/success')
   


@app.route('/show_recipe/<int:id>')
def show_recipe(id):
    if"logged_id" not in session:
        return redirect("/")
    data ={
        "id" : session['logged_id']
    }
    loged_user= User.user_by_id(data)
    print(id)
    data = {
        "id": id
        }
    recipe = Recipes_only.get_recipe_by_id(data)
    data_user={
        "id": recipe.user_id
        }
    creator_recipe=User.user_by_id(data_user)
    return render_template("onerecipe.html",recipe=recipe,loged_user=loged_user,creator_recipe=creator_recipe) 
   


# @app.route('/update_user/<int:id>', methods=["POST"])
# def update_user_post(id):
#     print(id)
#     data = {
#         "id": id,
#         "uname": request.form["uname"],
#         "ulastname": request.form["ulastname"],
#         "uemail": request.form["uemail"]
#         }
#     User.update(data)
#     print(f"/show_user/{id}")
#     return redirect(f"/show_user/{id}") # lo que me regreso de la base al html

#----------------------------------------------------UPDATE

# @app.route('/show_user/<int:id>')
# def show_user(id):
#     print(id)
#     data = {
#         "id": id,
    
#         }
#     user_id = User.get_user_by_id(data)
#     print(user_id)
#     return render_template("showuser.html",user= user_id) # lo que me regreso de la base al html
# #         # si es otra pagina 








# @app.route("/")
# def index():
#     users = User.get_all() # regresa los valores del metodo get all y almacena todos los datos de lbd
#     print(users)
#     return render_template("users.html",users=users) 

# @app.route("/newuser")
# def newuser():
#     return render_template("newuser.html")
 
 

# @app.route('/create_user', methods=["POST"])
# def create_user():
#     data = {
#         "uname": request.form["uname"],
#         "ulastname": request.form["ulastname"],
#         "uemail": request.form["uemail"]
#         # guarda los valores del formulario
#         }
   
#     id=User.save(data) # manda llamar al metodo para guardar
#     print(id)
   
#     return redirect(f"/show_user/{id}")# lo que me regreso de la base al html
#         # si es otra pagina 

# @app.route('/delete_user/<int:id>')
# def delete_user(id):
#     print(id)
#     data = {
#         "id": id
#         }
#     User.delete(data)
#     users = User.get_all()
#     return render_template("users.html",users=users)
   


# @app.route('/show_user/<int:id>')
# def show_user(id):
#     print(id)
#     data = {
#         "id": id,
    
#         }
#     user_id = User.get_user_by_id(data)
#     print(user_id)
#     return render_template("showuser.html",user= user_id) # lo que me regreso de la base al html
#         # si es otra pagina 

# @app.route('/update_user/<int:id>')
# def update_user(id):
#     print(id)
#     data = {
#         "id": id
#         }
#     user_id = User.get_user_by_id(data)
#     print(user_id)
#     return render_template("updateuser.html",user_id= user_id) # lo que me regreso de la base al html
#         # si es otra pagina 

# @app.route('/update_user/<int:id>', methods=["POST"])
# def update_user_post(id):
#     print(id)
#     data = {
#         "id": id,
#         "uname": request.form["uname"],
#         "ulastname": request.form["ulastname"],
#         "uemail": request.form["uemail"]
#         }
#     User.update(data)
#     print(f"/show_user/{id}")
#     return redirect(f"/show_user/{id}") # lo que me regreso de la base al html
#         # si es otra pagina 