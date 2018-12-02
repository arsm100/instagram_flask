from flask import jsonify, Blueprint, request
from instagram import app
from models.user import User

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    users = User.query.with_entities(User.id).all()

    users = [str(user[0]) for user in users]

    return jsonify(users)
