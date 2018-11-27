import re
from sqlalchemy import event
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from instagram import db, app
from instagram.helpers.utils import validation_preparation

class Donation(db.Model):
    __tablename__ = 'donations'

    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False, index=True)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'),
                        nullable=False, index=True)
    amount = db.Column(db.Numeric(), nullable=False)

    def __init__(self, donor_id, image_id, amount):
        self.donor_id = donor_id
        self.image_id = image_id
        self.amount = amount
