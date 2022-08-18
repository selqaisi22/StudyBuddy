from flask import Flask

app = Flask(__name__)
app.secret_key = "Ello"
DATABASE = "studybuddy_schema"