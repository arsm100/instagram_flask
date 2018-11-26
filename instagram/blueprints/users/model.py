import re
from sqlalchemy import event#, Table, Column, Integer, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from instagram import db, app
from instagram.helpers.utils import validation_preparation
from instagram.blueprints.images.model import Image

following_table = db.Table('followings', db.Model.metadata,
    db.Column('idol_id', db.Integer, db.ForeignKey('users.id'), index=True, nullable=False),
    db.Column('fan_id', db.Integer, db.ForeignKey('users.id'), index=True, nullable=False),
    db.Index('ix_unique_idol_fan', 'idol_id', 'fan_id', unique=True)
)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True,
                         unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(), index=True, nullable=False)
    description = db.Column(db.Text)
    profile_picture = db.Column(db.String())
    images = db.relationship('Image', backref='user', lazy=True, order_by="desc(Image.id)")
    private = db.Column(db.Boolean)


    #### DEFINING SELF REFERENTIAL MANY-TO-MANY RELATIONSHIP ####
    #### OPTION 1 ####
    ### Prefer this for beginners since it's more explicit
    fans = db.relationship("User",
                        secondary=following_table,
                        primaryjoin=id==following_table.c.idol_id,
                        secondaryjoin=id==following_table.c.fan_id
    )
    idols = db.relationship("User",
                    secondary=following_table,
                    primaryjoin=id==following_table.c.fan_id,
                    secondaryjoin=id==following_table.c.idol_id
    )

    #### OPTION 2 ####
    # fans = db.relationship("User",
    #                     secondary=following_table,
    #                     primaryjoin=id==following_table.c.idol_id,
    #                     secondaryjoin=id==following_table.c.fan_id,
    #                     backref = db.backref('idols')
    # )

    feed_images = db.relationship(Image,
                    secondary=following_table,
                    primaryjoin=id==following_table.c.fan_id,
                    secondaryjoin=following_table.c.idol_id==Image.user_id,
                    order_by="desc(Image.id)" # latest images first
    )



    def __init__(self, email, username, password):
        self.validation_errors = []
        self.email = email
        self.username = username
        self.password_hash = password

    def __repr__(self):
        return f"ID: {self.id} Username: {self.username} Email: {self.email}"

    @hybrid_property
    def profile_picture_url(self):
        if self.profile_picture:
            return f"{app.config['S3_LOCATION']}{self.profile_picture}"
        else:
            return f"{app.config['S3_LOCATION']}profile-placeholder.jpg"

    @validates('username')
    @validation_preparation
    def validate_username(self, key, username):
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
    @validation_preparation
    def validate_email(self, key, email):
        if not email:
            self.validation_errors.append('No email provided')

        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            self.validation_errors.append(
                'Provided email is not an email address')

        if (not self.email == email):
            if User.query.filter_by(email=email).first():
                self.validation_errors.append('Email is already in use')

        return email

    @validates('password_hash')
    @validation_preparation
    def set_password(self, key, password):
        if not password:
            self.validation_errors.append('Password not provided')

        # if not re.match('\d.*[A-Z]|[A-Z].*\d', password):
        #     raise AssertionError(
        #         'Password must contain 1 capital letter and 1 number')

        if len(password) < 8 or len(password) > 50:
            self.validation_errors.append(
                'Password must be between 8 and 50 characters')

        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def follow(self, user):
        if self == user:
            return False # cannot follow self

        if user in self.idols:
            return False # already following

        self.idols.append(user)
        db.session.add(self)
        db.session.commit()
        return True

    def unfollow(self, user):
        if self == user:
            return False

        if not user in self.idols:
            return False # not yet following, can't unfollow

        self.idols.remove(user)
        db.session.add(self)
        db.session.commit()
        return True
