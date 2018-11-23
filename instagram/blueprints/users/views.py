from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user
from instagram.blueprints.users.model import User
from instagram.blueprints.users.forms import NewUserForm, EditUserForm
from instagram import app, db
from instagram.helpers import upload_file_to_s3, allowed_profile_images, delete_file_from_s3
from werkzeug.utils import secure_filename


users_blueprint = Blueprint('users',
                            __name__)


@users_blueprint.route('/new', methods=['GET'])
def new():
    if current_user.is_authenticated:
        return redirect(url_for('users.edit', id=current_user.id))

    form = NewUserForm()
    return render_template('new.html', form=form)


@users_blueprint.route('/', methods=['POST'])
def create():
    form = NewUserForm(request.form)

    user = User(username=form.username.data,
                email=form.email.data,
                password=form.password.data)

    if len(user.validation_errors) > 0:
        return render_template('new.html', validation_errors=user.validation_errors, form=form)
    else:
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f"Welcome {user.username}")
        return redirect(url_for('users.show', username=user.username))


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.query.filter_by(username=username).first()

    if user:
        allowed_to_view_profile = not user.private or \
            (current_user.is_authenticated and current_user.id == user.id)
        return render_template('show.html', user=user, allowed_to_view_profile=allowed_to_view_profile)


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    edit_user_form = EditUserForm(obj=current_user)
    return render_template('edit.html', user=current_user, form=edit_user_form)


@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    form = EditUserForm(request.form)

    user = User.query.get(id)

    # Prevent unauthorized user from changing data of another user
    if not user.id == current_user.id:
        return render_template('edit.html', validation_errors=['Unauthorized!'], form=form, user=user)

    user.username = form.username.data
    user.email = form.email.data
    user.description = form.description.data
    user.private = form.private.data

    if len(user.validation_errors) > 0:
        return render_template('edit.html', validation_errors=user.validation_errors, form=form, user=user)
    else:
        db.session.add(user)
        db.session.commit()
        flash('Information updated!')
        return redirect(url_for('users.show', username=user.username))


@users_blueprint.route('/<id>/profile/image', methods=['POST'])
@login_required
def upload_profile_image(id):
    form = EditUserForm()

    user = User.query.get(id)

    # Prevent unauthorized user from changing data of another user
    if not user.id == current_user.id:
        return render_template('edit.html', validation_errors=['Unauthorized!'], form=form, user=user)

    if "profile_image" not in request.files:
        flash("No profile image")
        return render_template('edit.html', validation_errors=[], form=form, user=user)

    file = request.files["profile_image"]

    if file.filename == "":
        flash("Please select a file")
        return render_template('edit.html', form=form)

    if file and allowed_profile_images(file.filename):
        old_filename = user.profile_picture
        file.filename = secure_filename(user.username + "-" + file.filename)
        output = upload_file_to_s3(file, app.config["S3_BUCKET"])
        user.profile_picture = file.filename

        db.session.add(user)
        db.session.commit()

        delete_file_from_s3(old_filename, app.config["S3_BUCKET"])

        flash("Profile Picture Updated!")

        return redirect(url_for('users.show', username=user.username))

    else:
        return redirect("/")

@users_blueprint.route('/search', methods=['POST'])
def search():
    username = request.form["username"]
    user = User.query.filter_by(username=username).first()

    return redirect(url_for("users.show", username=user.username))
