from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash, session


class Note:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.information = data['information']
        self.topic_id = data['topic_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_one_note(cls, data):
        query = "SELECT * "
        query += "FROM notes "
        query += "WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) == 1:
            return cls(result[0])
        else:
            return None

    @classmethod
    def add_note(cls, data):
        query = "INSERT INTO notes(title, information, topic_id) "
        query +="VALUES(%(title)s, %(information)s, %(topic_id)s );"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def delete_note(cls, data):
        query = "DELETE FROM notes "
        query += "WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result
    
    @classmethod
    def update_note(cls, data):
        query = "UPDATE notes "
        query += "SET title = %(title)s, information = %(information)s "
        query += "WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result