from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash
import re


class Recipe:
    def __init__(self, data:dict) -> None:
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.instructions = data.get('instructions')
        self.date_cooked = data.get('date_cooked')
        self.under_30 = data.get('under_30')
        self.user_id = data.get('user_id')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    def __repr__(self):
        return f'<Recipe: {self.name}> Created by {self.user_id}'

    @staticmethod
    def validate_recipe(form:dict) -> bool:
        """Valides the recipe submitted by the user."""

        is_valid = True
        if not len(form.get('name')) > 0:
            flash('* Invalid Name.')
            is_valid = False
        if not len(form.get('description')) > 0:
            flash('* Invalid Description.')
            is_valid = False
        if not len(form.get('instructions')) > 0:
            flash('* Invalid Instructions.')
            is_valid = False
        if form.get('date_cooked', None) == None:
            flash('* Invalid Date.')
            is_valid = False
        if form.get('under_30', None) == None:
            flash('* Select an option for Over/Under 30.')
            is_valid = False

        return is_valid

    @classmethod
    def get_all_users_with_recipes(cls):
        """This method returns all users with recipes associated with them."""

        query = "SELECT * FROM recipes LEFT JOIN users ON user_id = users.id;"
        results = connectToMySQL('recipes').query_db(query)
        users = []

        for row in results:
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }

            user = User(user_data)

            recipe_data = {
                'id': row['id'],
                'name': row['name'],
                'description': row['description'],
                'instructions': row['instructions'],
                'date_cooked': row['date_cooked'],
                'under_30': row['under_30'],
                'user_id': row['user_id'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }

            user.recipes.append(Recipe(recipe_data))
            users.append(user)

        return users

    @classmethod
    def create_recipe(cls, data:dict) -> int:
        """Query to create the recipe and insert it into the database."""

        query = """INSERT INTO recipes (name, description, instructions, date_cooked, under_30, user_id)
                VALUES (%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under_30)s, %(user_id)s);"""
        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def find_by_id(cls, data:dict) -> object:
        """Query to find the recipe by id. Return an instance of the recipe."""

        query = "SELECT * FROM recipes WHERE id=%(id)s;"
        result = connectToMySQL('recipes').query_db(query, data)
        return cls(result[0])

    @classmethod
    def update_recipe(cls, data:dict) -> None:
        """Update the recipe in the database."""

        query = """UPDATE recipes SET 
                name=%(name)s, 
                description=%(description)s, 
                instructions=%(instructions)s,
                date_cooked=%(date_cooked)s,
                under_30=%(under_30)s
                WHERE id=%(id)s;"""

        connectToMySQL('recipes').query_db(query, data)

    @staticmethod
    def delete_recipe(data:dict) -> None:
        """Delete the recipe with provided id."""

        query = "DELETE FROM recipes WHERE id=%(id)s;"
        connectToMySQL('recipes').query_db(query, data)