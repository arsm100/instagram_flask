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

    images_feed = current_user.images_feed

    return render_template('feed/index.html', images_feed=images_feed)
