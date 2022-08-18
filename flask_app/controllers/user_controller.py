from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.topic_model import Topic
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/")
@app.route("/login/register")
def display_login_registration():
        return render_template("login_register.html")


@app.route("/register", methods=['POST'])
def register_user():
    if User.validate_registration(request.form) == False:
        return redirect("/login/register")
    else:
        if User.get_one({'email': request.form['email']}) == None:
            data = {
                "first_name": request.form['first_name'],
                "last_name": request.form['last_name'],
                "email" : request.form['email'],
                "password": bcrypt.generate_password_hash(request.form['password'])
            }
            user_id = User.create_user(data)
            session['first_name'] = request.form['first_name']
            session['last_name'] = request.form['last_name']
            session['email'] = request.form['email']
            session['user_id']=user_id
            return redirect("/dashboard")
        else:
            flash("This email is already in use, please type a different email or login", "error_email_registration")
            return redirect("/login/register")
    
@app.route("/login", methods=["POST"])
def login_user():
    if User.validate_login(request.form) == False:
        return redirect("/login/register")
    else:
        result = User.get_one(request.form)
        if result == None:
            flash("Wrong credentials.", "error_login")
            return redirect("/login/register")
        else:
            if not bcrypt.check_password_hash( result.password, request.form['password']):
                flash("Wrong credentials.", "error_login")
                return redirect("/login/register")
            else:
                session['first_name'] = result.first_name
                session['last_name'] = result.last_name
                session['email'] = result.email
                session['user_id'] = result.id
                session['user_dictionary'] = {
                    'id' : result.id,
                    'first_name' : result.first_name,
                    'last_name' : result.last_name,
                    'email' : result.email
                }
                return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if User.validate_session() == False:
        return redirect("/login/register")
    else:
        data = {
            "id": session['user_id']
        }
        topics_list = Topic.get_all_topics(data)
        if topics_list != None:
            return render_template("dashboard.html", topics_list = topics_list)
        else:
            return render_template("dashboard.html", topics_list = [])
        

@app.route("/logout")
def user_logout():
    session.clear()
    return redirect("/login/register")