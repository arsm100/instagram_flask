from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField

class NewUserForm(FlaskForm):

    username = StringField('Username:')
    email = StringField('Email:')
    password = PasswordField('Password:')
    submit = SubmitField('Add User')


class EditUserForm(FlaskForm):

    username = StringField('Username:')
    email = StringField('Email:')
    submit = SubmitField('Update Information')


