from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash, session

class Card:
    def __init__(self, data):
        self.id = data['id']
        self.word = data['word']
        self.description = data['description']
        self.topic_id = data['topic_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_all_cards(cls, data):
        query = "SELECT * "
        query +="FROM topics "
        query += "JOIN cards ON topics.id = cards.topic_id "
        query += "WHERE topic_id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) > 0:

            one_topic = cls(result[0])
            one_topic.cards = []
            for row in result:
                card_columns = {
                    "id": row['cards.id'],
                    "word" : row['word'],
                    "description" : row['description'],
                    "topic_id" : row['topic_id'],
                    "created_at": row['cards.created_at'],
                    "updated_at": row['cards.updated_at']
                }
                
                card = cls(card_columns)
                one_topic.cards.append(card)

            return one_topic
        else:
            return None

    @classmethod
    def get_one_card(cls, data):
        query = "SELECT * "
        query += "FROM cards "
        query += "WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) == 1:
            return cls(result[0])
        else:
            return None


    @classmethod
    def add_card(cls, data):
        query = "INSERT INTO cards(word, description, topic_id) "
        query +="VALUES(%(word)s, %(description)s, %(topic_id)s );"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def delete_card(cls, data):
        query = "DELETE FROM cards "
        query += "WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result
    
    @classmethod
    def update_card(cls, data):
        query = "UPDATE cards "
        query += "SET word = %(word)s, description = %(description)s "
        query += "WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result