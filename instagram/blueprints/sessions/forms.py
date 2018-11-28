from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators


class SignInForm(FlaskForm):

    username = StringField('Username:', [validators.InputRequired()])
    password = PasswordField('Password:', [validators.InputRequired()])
    submit = SubmitField('Sign In')
