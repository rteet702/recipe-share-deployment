from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re


NAME_REGEX = re.compile(r'^[a-zA-Z]{2,}$')
PASSWORD_REGEX = re.compile(r'^[a-zA-Z0-9!@#$%^&*()-_+]{8,}$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:

    """
    This class represents a typical user. All methods inside this class will pertain to the User, as well as any related data.
    Tentatively, this class will be set up to handle the storing of 'Recipe' instances.
    """

    def __init__(self, data:dict) -> None:
        self.id = data.get('id')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.email = data.get('email')
        self.password = data.get('password')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.recipes = []

    def __repr__(self):
        return f'{self.email}'

    @staticmethod
    def register_user(data:dict) -> None:
        """Pick up data from the user submitted form, and insert it into a database."""

        query = """INSERT INTO users (first_name, last_name, email, password)
                    VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        connectToMySQL('recipes').query_db(query, data)

    @staticmethod
    def validate_registration(form:dict) -> bool:
        """Validates the registration form submitted by the user when creating an account."""

        is_valid = True

        email_data = {'email': form.get('email_registration')}

        if User.get_by_email(email_data):
            flash('* Email is already registered.', 'registration')
            is_valid = False
        if not EMAIL_REGEX.match(form.get('email_registration')):
            flash('* Please enter a valid email.', 'registration')
            is_valid = False
        if not NAME_REGEX.match(form.get('first_name')):
            flash('* First name must be at least 2 characters.', 'registration')
            is_valid = False
        if not NAME_REGEX.match(form.get('last_name')):
            flash('* Last name must be at least 2 characters.', 'registration')
            is_valid = False
        if not PASSWORD_REGEX.match(form.get('password_registration')):
            flash('* Password must consist of alphanumeric or special characters, and must be 8 characters or longer.', 'registration')
            is_valid = False
        if form.get('password_registration') != form.get('password_confirmation', 'registration'):
            flash('* Password do not match.')
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(form:dict) -> bool:
        """Validates the login form submitted by the user."""

        is_valid = True

        email_data = {'email': form.get('email_login')}

        if not User.get_by_email(email_data):
            flash('* Email is not registered.','login')
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls, data:dict):
        """Check if there is an user associated with the provided email. If a user is found, returns an object constructed from the query."""

        query = "SELECT * FROM users WHERE email=%(email)s;"
        result = connectToMySQL('recipes').query_db(query, data)
        if not result:
            return False

        return cls(result[0])

    @classmethod
    def get_by_id(cls, data:dict):
        """Access the user associated with the provided id. If a user is found, returns an object constructed from the query."""

        query = "SELECT * FROM users WHERE id=%(id)s;"
        result = connectToMySQL('recipes').query_db(query, data)
        if result:
            return cls(result[0])

    @classmethod
    def get_user_by_recipe(cls, data:dict) -> object:
        """Get user by recipe."""

        query = "SELECT user_id FROM recipes WHERE id=%(id)s;" 
        result = connectToMySQL('recipes').query_db(query, data)

        user_data = {'id': result[0]['user_id']}
        return cls.get_by_id(user_data)