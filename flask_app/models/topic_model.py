from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash, session
from flask_app.models.note_model import Note

class Topic:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    @classmethod
    def get_all_topics(cls, data):
        query = "SELECT * "
        query +="FROM topics "
        query +="WHERE user_id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) > 0:
            topics = []
            for row in result:
                topics.append(cls(row))
            return topics
        else:
            return None

    @classmethod
    def get_all_notes(cls, data):
        query = "SELECT * "
        query +="FROM topics "
        query += "JOIN notes ON topics.id = notes.topic_id "
        query += "WHERE topic_id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) > 0:

            one_topic = cls(result[0])
            one_topic.notes = []
            for row in result:
                note_columns = {
                    "id": row['notes.id'],
                    "title" : row['title'],
                    "information" : row['information'],
                    "topic_id" : row['topic_id'],
                    "created_at": row['notes.created_at'],
                    "updated_at": row['notes.updated_at']
                }
                
                note = Note(note_columns)
                one_topic.notes.append(note)

            return one_topic
        else:
            return None


    @classmethod
    def add_topic(cls, data):
        query = "INSERT INTO topics(name, user_id) "
        query +="VALUES(%(name)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_one_topic(cls, data):
        query = "SELECT * "
        query += "FROM topics "
        query += "WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) == 1:
            return cls(result[0])
        else:
            return None
    
    @classmethod
    def delete_topic(cls, data):
        query = "DELETE FROM topics "
        query += "WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result