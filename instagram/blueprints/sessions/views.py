from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from instagram.blueprints.users.model import User
from instagram.blueprints.sessions.forms import SignInForm
from instagram import app

sessions_blueprint = Blueprint('sessions',
                               __name__,
                               template_folder='templates/sessions')


@sessions_blueprint.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash('You were successfully signed in')
            return redirect(url_for('users.show', username=user.username))
        else:
            flash('Wrong username/email')

    return render_template('sign_in.html', form=form)


@sessions_blueprint.route('/sign_out', methods=['POST'])
@login_required
def sign_out():
    logout_user()
    flash('You were successfully signed out')
    return redirect(url_for('users.new'))
