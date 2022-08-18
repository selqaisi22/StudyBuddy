from flask import session, request, redirect, render_template, flash
from flask_app import app
from flask_app.models import card_model
from flask_app.models.user_model import User
from flask_app.models.topic_model import Topic

@app.route("/cards/<int:id>")
def display_all_cards(id):
    if User.validate_session == False:
        return redirect("/login/register")
    else:
        data = {
            "id": id
        }
        one_topic = card_model.Card.get_all_cards(data)
        current_topic = Topic.get_one_topic(data)
        return render_template("cards.html", one_topic=one_topic, current_topic = current_topic)

@app.route("/card/new/<int:id>")
def display_add_card(id):
    if User.validate_session == False:
        return redirect("/login/register")
    else:
        data = {
            "id": id
        }
        topic = Topic.get_one_topic(data)
        return render_template("new_card.html", topic = topic)

@app.route("/card/new/<int:id>", methods=['POST'])
def add_card(id):
    data = {
        "word": request.form['word'],
        "description": request.form['description'],
        "topic_id" : id
    }
    card_model.Card.add_card(data)
    return redirect(f"/cards/{id}")

@app.route("/card/delete/<int:id>/<int:tid>")
def delete_card(id, tid):
    data = {
        "id": id,
    }
    print(tid)
    card_model.Card.delete_card(data)
    return redirect(f"/cards/{tid}")

@app.route("/card/edit/<int:id>/<int:tid>")
def display_edit_card(id, tid):
    if User.validate_session() == False:
        return redirect("/logout/register")
    else:
        data = {
            "id": id
        }
        card = card_model.Card.get_one_card(data)
        return render_template("update_card.html", card = card)

@app.route("/card/edit/<int:id>/<int:tid>", methods=['POST'])
def edit_card(id, tid):
    data = {
        "word": request.form['word'],
        "description": request.form['description'],
        "id" : id
    }
    card_model.Card.update_card(data)
    return redirect(f"/cards/{tid}")