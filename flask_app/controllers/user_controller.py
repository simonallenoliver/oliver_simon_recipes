from flask import Flask, render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)  

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/registration', methods=['POST'])
def registration():

    if not User.validate_user(request.form):
      return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    new_account = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
        }

    user_id = User.save(new_account)
    
    session['user_id'] = user_id    
    return redirect('/user_page')


@app.route('/user_page')
def user_page():
    if 'user_id' in session:
        user_id = session['user_id']

        data = {
        'user_id': user_id
        }
        current_user = User.get_user_by_id(data)
        return render_template("user_page.html", current_user = current_user, recipes = Recipe.get_recipes_users())
    else:
        return redirect('/')


@app.route('/login', methods=["POST"])
def login():
    data = {
    'email' : request.form['email']
    }
    user_in_db = User.getbyemail(data)

    if not user_in_db:
        flash("incorrect email or password", "login")
        return redirect('/')

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("incorrect email or password", "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/user_page')

@app.route('/logout')
def destroy_session():
    session.clear()
    return redirect('/')