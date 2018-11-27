from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField, validators


class NewUserForm(FlaskForm):

    username = StringField('Username:')
    email = StringField('Email:')
    password = PasswordField('Password:')
    submit = SubmitField('Add User')


class EditUserForm(FlaskForm):

    username = StringField('Username:')
    email = StringField('Email:')
    description = TextAreaField('Description:')
    private = BooleanField('Make Private')
    submit = SubmitField('Update Information')

class SearchUserForm(FlaskForm):

    username = StringField('Username:', [validators.InputRequired()])
    submit = SubmitField('Search')
