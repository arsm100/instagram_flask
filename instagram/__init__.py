import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import config

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

# https://stackoverflow.com/questions/38795414/flask-sqlalchemy-disable-autoflush-for-the-whole-session
db = SQLAlchemy(app, session_options={"autoflush": False})
# db = SQLAlchemy(app)

Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "sessions.sign_in"

from instagram.users.model import User
from instagram.images.model import Image


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None


@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("users.show", username=current_user.username))
    else:
        return redirect(url_for("sessions.sign_in"))


# NOTE! These imports need to come after you've defined db, otherwise you will
# get errors in your models.py files.
# Grab the blueprints from the other views.py files for each "app"
from instagram.users.views import users_blueprint
from instagram.sessions.views import sessions_blueprint
from instagram.images.views import images_blueprint

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix='/')
app.register_blueprint(images_blueprint, url_prefix='/images')
