import re
from sqlalchemy.orm import validates
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from instagram import db


# @login_manager.user_loader
# def load_user(user_id):
#     try:
#         return User.query.get(user_id)
#     except:
#         return None


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True,
                         unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(), index=True, nullable=False)

    def __init__(self, email, username, password):
        self.validation_errors = []
        self.email = email
        self.username = username
        self.set_password(password)

    def __repr__(self):
        return f"{self.username} with email {self.email} saved to database!"

    @validates('username')
    def validate_username(self, key, username):
        try:
            self.validation_errors
        except AttributeError:
            self.validation_errors = []

        if not username:
            self.validation_errors.append('No username provided')

        if (not self.username == username):
            if User.query.filter_by(username=username).first():
                self.validation_errors.append('Username is already in use')

        if len(username) < 5 or len(username) > 20:
            self.validation_errors.append(
                'Username must be between 5 and 20 characters')

        return username

    @validates('email')
    def validate_email(self, key, email):
        try:
            self.validation_errors
        except AttributeError:
            self.validation_errors = []

        print("-------> 2a ---->")

        if not email:
            self.validation_errors.append('No email provided')

        print("-------> 2b ---->")

        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            self.validation_errors.append(
                'Provided email is not an email address')

        print("-------> 2c ---->")

        if (not self.email == email):
            print("-------> 2d ---->")

            if User.query.filter_by(email=email).first():
                print("-------> 2e ---->")

                self.validation_errors.append('Email is already in use')

        return email

    def set_password(self, password):
        try:
            self.validation_errors
        except AttributeError:
            self.validation_errors = []

        if not password:
            self.validation_errors.append('Password not provided')

        # if not re.match('\d.*[A-Z]|[A-Z].*\d', password):
        #     raise AssertionError(
        #         'Password must contain 1 capital letter and 1 number')

        if len(password) < 8 or len(password) > 50:
            self.validation_errors.append(
                'Password must be between 8 and 50 characters')

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
