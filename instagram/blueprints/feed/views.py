from flask import Blueprint, render_template
from flask_login import current_user


feed_blueprint = Blueprint('feed',
                            __name__,
                            template_folder='templates')


@feed_blueprint.route('/', methods=['GET'])
def index():
    if not current_user.is_authenticated:
        flash("Sign in first")
        return redirect(url_for('sessions.sign_in'))

    feed_images = current_user.feed_images

    return render_template('feed/index.html', feed_images=feed_images)
