from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort

from app.mod_offer.forms import CreateOfferForm

from app import db

from app.model import offer

mod_offer = Blueprint('offer', __name__, url_prefix='/offer')


@mod_offer.route('/', methods=['GET'])
def index():
    return render_template('offer/index.html')


@mod_offer.route('/', methods=['POST'])
def create():
    return '201'

@mod_offer.route('/create/', methods=['GET'])
def create_form():
    form = CreateOfferForm()
    return render_template('offer/create.html', form=form)

@mod_offer.route('/<int:offer_id>/', methods=['GET'])
def show_offer(offer_id=None):
    if offer_id == 1:
        abort(404)
    else:
        return render_template('offer/show.html')
