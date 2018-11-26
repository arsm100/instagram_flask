from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from instagram.blueprints.users.model import User
from instagram.blueprints.sessions.forms import SignInForm
from instagram import app
from instagram.helpers.google_oauth import oauth

sessions_blueprint = Blueprint('sessions',
                               __name__,
                               template_folder='templates/sessions')


@sessions_blueprint.route('/sign_in/google')
def google_sign_in():
    redirect_uri = url_for('sessions.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route('/authorize/google')
def authorize():
    token = oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.query.filter_by(email=email).first()

    if user:
        login_user(user)
        flash('You were successfully signed in')
        return redirect(url_for('users.show', username=user.username))
    else:
        form = SignInForm()
        flash('Please try signing in/up again or contact support')
        return render_template('sign_in.html', form=form)

@sessions_blueprint.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash('You were successfully signed in')
            return redirect(url_for('feed.index'))
        else:
            flash('Wrong username/email')

    return render_template('sign_in.html', form=form)


@sessions_blueprint.route('/sign_out', methods=['POST'])
@login_required
def sign_out():
    logout_user()
    flash('You were successfully signed out')
    return redirect(url_for('users.new'))
