from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from instagram.blueprints.users.model import User
from instagram.blueprints.images.model import Image
from instagram.blueprints.donations.model import Donation
from instagram import app, db
from instagram.helpers.braintree import gateway


donations_blueprint = Blueprint('donations',
                             __name__,
                             template_folder='templates')


@donations_blueprint.route('/', methods=['POST'])
@login_required
def create():
    nonce_from_the_client = request.form["payment_method_nonce"]

    result = gateway.transaction.sale({
        "amount": request.form['amount'],
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })

    if result.is_success:
        donation = Donation(donor_id=current_user.id, image_id=request.form['image_id'], amount=request.form['amount'])

        db.session.add(donation)
        db.session.commit()
        flash(f"Your donation of {donation.amount} has been successfully sent!")
        return redirect(request.referrer)
    else:
        flash(result.message)

        return redirect(request.referrer)
