from flask import jsonify, Blueprint, request
from instagram import app
from models.image import Image
from models.user import User

images_api_blueprint = Blueprint('images_api',
                             __name__,
                             template_folder='templates')

def url(image_name):
    return app.config['S3_LOCATION'] + image_name

@images_api_blueprint.route('/', methods=['GET'])
def index():
    if request.args.get('userId'):
        images = Image.query.with_entities(Image.image_name).add_columns(url(Image.image_name)).filter_by(user_id = int(request.args['userId'])).all()
    else:
        images = Image.query.with_entities(Image.image_name).add_columns(url(Image.image_name)).all()

    images = [image[1] for image in images]

    return jsonify(images)
