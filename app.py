import os
import re
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "sign_in"


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None


class NewUserForm(FlaskForm):

    username = StringField('Username:')
    email = StringField('Email:')
    password = PasswordField('Password:')
    submit = SubmitField('Add User')


class EditUserForm(FlaskForm):

    username = StringField('Username:')
    email = StringField('Email:')
    submit = SubmitField('Update Information')


class SignInForm(FlaskForm):

    username = StringField('Username:', [validators.InputRequired()])
    password = PasswordField('Password:', [validators.InputRequired()])
    submit = SubmitField('Sign In')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/users/new', methods=['GET'])
def new_user():
    if current_user.is_authenticated:
        return redirect(url_for('edit_user', id=current_user.id))

    form = NewUserForm()
    return render_template('new.html', form=form)


@app.route('/users', methods=['POST'])
def create_user():
    print(request.form)
    form = NewUserForm(request.form)

    user = User(username=form.username.data,
                email=form.email.data,
                password=form.password.data)

    if user.validation_errors:
        return render_template('new.html', validation_errors=user.validation_errors, form=form)
    else:
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f"Welcome {user.username}")
        return redirect(url_for('edit_user', id=user.id))


@app.route('/users/<id>/edit', methods=['GET'])
@login_required
def edit_user(id):
    edit_user_form = EditUserForm(obj=current_user)
    return render_template('edit.html', user=current_user, form=edit_user_form)


@app.route('/users/<id>', methods=['POST'])
@login_required
def update_user(id):
    form = EditUserForm(request.form)

    user = User.query.get(id)

    # Prevent unauthorized user from changing data of another user
    if not user.id == current_user.id:
        return render_template('edit.html', validation_errors=['Unauthorized!'], form=form)

    user.username = form.username.data
    user.email = form.email.data

    if user.validation_errors:
        return render_template('edit.html', validation_errors=user.validation_errors, form=form)
    else:
        db.session.add(user)
        db.session.commit()
        flash('Information updated!')
        return redirect(url_for('edit_user', id=user.id))


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash('You were successfully signed in')
            return redirect(url_for('edit_user', id=user.id))
        else:
            flash('Wrong username/email')

    return render_template('sign_in.html', form=form)


@app.route('/sign_out', methods=['POST'])
@login_required
def sign_out():
    logout_user()
    flash('You were successfully signed out')
    return redirect(url_for('new_user'))


def validation_preparation(func):
    def wrapper(obj, key, value):
        try:
            obj.validation_errors
        except AttributeError:
            obj.validation_errors = []

        with db.session.no_autoflush:
            func(obj, key, value)

    return wrapper


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
    @validation_preparation
    def validate_username(self, key, username):
        if not username:
            self.validation_errors.append('No username provided')

        if (not self.username == username) and User.query.filter(User.username == username).first():
            self.validation_errors.append('Username is already in use')

        if len(username) < 5 or len(username) > 20:
            self.validation_errors.append(
                'Username must be between 5 and 20 characters')

        return username

    @validates('email')
    @validation_preparation
    def validate_email(self, key, email):
        if not email:
            self.validation_errors.append('No email provided')

        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            self.validation_errors.append(
                'Provided email is not an email address')

        if (not self.email == email) and User.query.filter(User.email == email).first():
            self.validation_errors.append('Email is already in use')

        return email

    def set_password(self, password):
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


if __name__ == '__main__':
    app.run()
