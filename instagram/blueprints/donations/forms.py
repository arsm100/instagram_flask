from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField


class DonationForm(FlaskForm):

    image_id = HiddenField('Image ID')
    password = PasswordField('Password:')
    submit = SubmitField('Add User')
