from flask import session, request, redirect, render_template, flash
from flask_app import app
from flask_app.models.note_model import Note
from flask_app.models.user_model import User
from flask_app.models.topic_model import Topic



@app.route("/notes/<int:id>")
def display_all_notes(id):
    if User.validate_session() == False:
        return redirect("/login/register")
    else:
        data = {
            "id": id
        }
        one_topic = Topic.get_all_notes(data)
        current_topic = Topic.get_one_topic(data)
        return render_template("notes.html", one_topic = one_topic, current_topic=current_topic) 

@app.route("/note/new/<int:id>")
def display_add_note(id):
    if User.validate_session() == False:
        return redirect("/logout/register")
    else:
        data = {
            "id": id
        }
        topic = Topic.get_one_topic(data)
        return render_template("new_note.html", topic = topic)

@app.route("/note/new/<int:id>", methods=['POST'])
def add_note(id):
    data = {
        "title": request.form['title'],
        "information": request.form['information'],
        "topic_id" : id
    }
    Note.add_note(data)
    return redirect(f"/notes/{id}")


@app.route("/note/delete/<int:id>/<int:tid>")
def delete_note(id, tid):
    data = {
        "id": id
    }
    Note.delete_note(data)
    return redirect(f"/notes/{tid}")

@app.route("/note/edit/<int:id>/<int:tid>")
def display_edit_note(id, tid):
    if User.validate_session() == False:
        return redirect("/logout/register")
    else:
        data = {
            "id": id
        }
        note = Note.get_one_note(data)
        return render_template("update_note.html", note = note)

@app.route("/note/edit/<int:id>/<int:tid>", methods=['POST'])
def edit_note(id, tid):
    data = {
        "title": request.form['title'],
        "information": request.form['information'],
        "id" : id
    }
    Note.update_note(data)
    return redirect(f"/notes/{tid}")