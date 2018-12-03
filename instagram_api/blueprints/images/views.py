from flask import jsonify, Blueprint, request, make_response
from models.image import Image
from models.user import User

images_api_blueprint = Blueprint('images_api',
                             __name__,
                             template_folder='templates')


@images_api_blueprint.route('/', methods=['GET'])
def index():
    if request.args.get('userId'):
        images = Image.query.with_entities(Image.image_name).add_columns(Image.url(Image.image_name)).filter_by(user_id = int(request.args['userId'])).all()
    else:
        images = Image.query.with_entities(Image.image_name).add_columns(Image.url(Image.image_name)).all()

    images = [image[1] for image in images]

    return jsonify(images)

@images_api_blueprint.route('/me', methods=['GET'])
def show():
    auth_header = request.headers.get('Authorization')

    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        responseObject = {
            'status': 'failed',
            'message': 'No authorization header found'
        }

        return make_response(jsonify(responseObject)), 401

    user_id = User.decode_auth_token(auth_token)

    user = User.query.get(user_id)

    if user:
        images = Image.query.with_entities(Image.image_name).add_columns(Image.url(Image.image_name)).filter_by(user_id = user.id).all()
        images = [image[1] for image in images]

        return jsonify(images)
    else:
        responseObject = {
            'status': 'failed',
            'message': 'Authentication failed'
        }

        return make_response(jsonify(responseObject)), 401
