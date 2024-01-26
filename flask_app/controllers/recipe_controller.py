from flask import Flask, render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)



@app.route('/create_page')
# the return gives us a template, plus the variable recipes (which used a Recipe class method to retrieve data) 
# which we then can use in our html to display information from our DB
def create_page():
        return render_template("create_page.html")


@app.route('/make_recipe', methods = ["POST"])
def make_recipe():
    new_recipe = {
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'under30' : request.form['under30'],
        'user_id' : session["user_id"]
        }

    Recipe.save(new_recipe)

    return redirect('/user_page') 


@app.route('/view_recipe/<int:id>')
def view_recipe(id):
        recipe = Recipe.get_one(id)
        
        id = recipe.user_id

        print("this is id", id)
        user= User.get_by_id(id)
        print("this is user", user)
        return render_template("view_recipe.html", recipe = recipe, user=user)


@app.route('/edit_page/<int:id>')
def edit_page(id):

    print("this is the session id", session["user_id"])
    recipe = Recipe.get_one(id)
    print("this is recipe", recipe)
    return render_template("edit_page.html", recipe = recipe)


@app.route("/update", methods = ["POST"])
def update():
    Recipe.update(request.form)
    return redirect("/user_page")

@app.route("/delete/<int:id>")
def delete(id):
    Recipe.delete(id)
    return redirect('/user_page')