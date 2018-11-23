from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from instagram.blueprints.users.model import User
from instagram.blueprints.images.model import Image
from instagram import app, db
from instagram.helpers import upload_file_to_s3, delete_file_from_s3, allowed_images
from werkzeug.utils import secure_filename


images_blueprint = Blueprint('images',
                             __name__)


@images_blueprint.route('/', methods=['POST'])
@login_required
def create():
    if "image" not in request.files:
        flash("No image")
        return redirect(url_for("users.show", username=current_user.username))

    file = request.files["image"]

    if file and allowed_images(file.filename):
        file.filename = secure_filename(
            str(current_user.id) + "-" + file.filename)
        output = upload_file_to_s3(file, app.config["S3_BUCKET"])

        image = Image(user_id=current_user.id, image_name=file.filename)

        db.session.add(image)
        db.session.commit()

        flash("Image Posted!")

        return redirect(url_for('users.show', username=current_user.username))

    else:
        flash("Failed. Try again!")
        return redirect("/")


@images_blueprint.route('/<id>', methods=['POST'])
@login_required
def destroy(id):
    image = Image.query.get(id)

    if not image.user.id == current_user.id:
        flash("The image doesn't belong to you!")
        return redirect(url_for("users.show", username=current_user.username))

    delete_file_from_s3(image.image_name, app.config["S3_BUCKET"])

    db.session.delete(image)
    db.session.commit()

    flash("Image deleted!")
    return redirect(url_for("users.show", username=current_user.username))
