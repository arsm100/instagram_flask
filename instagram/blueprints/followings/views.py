from flask import Blueprint, render_template, redirect, flash, request, url_for
from flask_login import current_user
from models.user import User

followings_blueprint = Blueprint('followings',
                            __name__,
                            template_folder='templates')


@followings_blueprint.route('/', methods=['GET'])
def show():
    if not current_user.is_authenticated:
        flash("Sign in first")
        return redirect(url_for('sessions.sign_in'))

    return render_template('followings/show.html')

@followings_blueprint.route('/', methods=['POST'])
def create():
    if not current_user.is_authenticated:
        flash("Sign in first")
        return redirect(url_for('sessions.sign_in'))

    fan_id = request.form.get('fan_id')

    if fan_id:
        fan = User.query.get(fan_id)
        if fan and current_user.approve(fan):
            print("------------")
            flash(f"You've approved {fan.username}")
            return redirect(request.referrer)

    idol = User.query.get(request.form['idol_id'])

    if idol and current_user.follow(idol) == 'Your request has been sent':
        flash(f"Your request to follow {idol.username} has been sent")
        return redirect(request.referrer)

    elif idol and current_user.follow(idol):
        flash(f"Successfully followed {idol.username}")
        return redirect(request.referrer)

    flash("Failed to follow user")
    return redirect(request.referrer)

@followings_blueprint.route('/<idol_id>', methods=['POST'])
def destroy(idol_id):
    if not current_user.is_authenticated:
        flash("Sign in first")
        return redirect(url_for('sessions.sign_in'))

    idol = User.query.get(idol_id)

    if idol and current_user.unfollow(idol):
        flash(f"Successfully unfollowed {idol.username}")
        return redirect(request.referrer)

    flash("Failed to unfollow user")
    return redirect(request.referrer)
