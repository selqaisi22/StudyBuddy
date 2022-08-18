from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models import user_model
from flask_app.models import topic_model



@app.route("/topic/new")
def display_add_topic():
    if user_model.User.validate_session() == False:
        return redirect("/login/register")
    else:
        return render_template("new_topic.html")


@app.route("/topic/new", methods = ['POST'])
def add_topic():
    data = {
        "name": request.form['name'],
        "user_id": session['user_id']
    }
    topic_model.Topic.add_topic(data)
    return redirect("/dashboard")

@app.route("/topic/delete/<int:id>")
def delete_topic(id):
    data = {
        "id": id
    }
    topic_model.Topic.delete_topic(data)
    return redirect("/dashboard")

