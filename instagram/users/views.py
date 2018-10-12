from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user
from instagram.models import User
from instagram.users.forms import NewUserForm, EditUserForm
from instagram import app, db


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates/users')


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
        return redirect(url_for('users.edit', id=user.id))


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
        return render_template('edit.html', validation_errors=['Unauthorized!'], form=form)

    user.username = form.username.data

    user.email = form.email.data

    if len(user.validation_errors) > 0:
        return render_template('edit.html', validation_errors=user.validation_errors, form=form)
    else:
        db.session.add(user)
        db.session.commit()
        flash('Information updated!')
        return redirect(url_for('users.edit', id=user.id))
