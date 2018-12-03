from flask import jsonify, Blueprint, request
from models.user import User

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    users = User.query.all()

    # there is probably a more efficient to do this
    users = [{"id": int(user.id), "username": user.username, "profileImage": user.profile_picture_url} for user in users]

    return jsonify(users)
