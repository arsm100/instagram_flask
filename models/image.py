import re
from sqlalchemy import event
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from instagram import db, app
from instagram.helpers.utils import validation_preparation


class Image(db.Model, UserMixin):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    image_name = db.Column(db.String(), nullable=False)

    def __init__(self, user_id, image_name):
        self.user_id = user_id
        self.image_name = image_name

    @hybrid_property
    def image_url(self):
        return f"{app.config['S3_LOCATION']}{self.image_name}"
