import datetime

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort

from app.mod_offer.forms import CreateOfferForm

from app import db

from app.model import offer
from app.model.offer import Offer, Photo
from app.model.user import User
from app.mod_auth.autorization_required import requires_sign_in
from app.model.validator import ValidationError, CombinedValidator, OfferValidator

import uuid
import os

mod_offer = Blueprint('offer', __name__, url_prefix='/offer')


def logged_user():
    if 'username' in session:
        return User.query.filter_by(email=session['username']).first()
    else:
        return None


@mod_offer.route('/', methods=['GET'])
def index():
    query = Offer.query.filter(Offer.is_sold == False).order_by(Offer.utc_publish_date.desc())

    offers = query.all()
    return render_template('offer/index.html', offers=offers)


@mod_offer.route('/', methods=['POST'])
@requires_sign_in()
def create():

    offer = Offer()
    offer.city = request.form['city']
    offer.street = request.form['street']
    offer.building_number = request.form['building_number']
    offer.apartment_number = int(request.form['apartment_number'])
    offer.room_count = int(request.form['room_count'])
    offer.area = int(request.form['area'])
    offer.tier = int(request.form['tier'])
    offer.has_balcony = 'has_balcony' in request.form and request.form['has_balcony'] == 'on'
    offer.description = request.form['description']
    offer.price = int(request.form['price'])
    offer.owner_id = session['user_id']
    offer.utc_publish_date = datetime.datetime.now()
    offer.is_sold = False

    validator = OfferValidator(lambda: offer)

    errors, valid = validator.validate()
    if not valid:
        for e in errors:
            flash(e.message)
        return redirect(url_for('offer.create_form'))

    db.session.add(offer)
    db.session.commit()

    for fname in request.files:
        file = request.files[fname]
        if file.filename == '':
            continue

        _, ext = os.path.splitext(file.filename)
        storename = uuid.uuid4().hex + ext
        file.save('C:\\code\\put\\kwadrat\\src\\app\\static\\' + storename)

        photo = Photo()
        photo.offer_id = offer.id
        photo.filename = storename

        db.session.add(photo)

    db.session.commit()

    flash("Dodano ogłoszenie")

    return redirect(url_for("offer.show_offer", offer_id=offer.id))



@mod_offer.route('/create/', methods=['GET'])
@requires_sign_in()
def create_form():
    return render_template('offer/create.html')


@mod_offer.route('/<int:offer_id>', methods=['GET'])
def show_offer(offer_id=None):
    offer = Offer.query.get(offer_id)
    if offer is None:
        abort(404)
    else:
        return render_template('offer/show.html', offer=offer)

def CreateFilter(param_name, param_desc, param_func, column):
    return GenericFilter(param_func, param_name, param_desc, column)


class GenericFilter(object):
    def __init__(self, params, param_name, param_desc, column):
        self.param_desc = param_desc
        self.param_name = param_name
        self.column = column
        self.param_func = params

    def validate(self):
        params = self.param_func()
        self.enabled = params.get(self.param_name + '_enabled', 'off') == 'on'
        lower = params.get(self.param_name + '_lower', '')
        upper = params.get(self.param_name + '_upper', '')

        if not self.enabled:
            return [], True

        if lower.isdigit() and upper.isdigit():
            if int(lower) <= int(upper):
                self.lower_val = int(lower)
                self.upper_val = int(upper)
                return [], True

        return [ValidationError('Niepoprawny przedział: ' + self.param_desc)], False

    def filter(self, query):
        if self.enabled and self.validate()[1]:
            return query.filter(self.column.between(self.lower_val, self.upper_val))
        return query


# class RoomFilter(object):
#     def __init__(self, params):
#         self.param_func = params
#
#     def validate(self):
#         params = self.param_func()
#         self.enabled = params.get('room_count_enabled', 'off') == 'on'
#         lower = params.get('room_count_lower', '')
#         upper = params.get('room_count_upper', '')
#
#         if not self.enabled:
#             return [], True
#
#         if lower.isdigit() and upper.isdigit():
#             if int(lower) <= int(upper):
#                 self.lower_val = int(lower)
#                 self.upper_val = int(upper)
#                 return [], True
#
#         return [ValidationError('Niepoprawny przedział: liczba pokoi')], False
#
#     def filter(self, query):
#         if self.enabled:
#             return query.filter(Offer.room_count.between(self.lower_val, self.upper_val))
#         return query

@mod_offer.route('/my/',methods=['GET'])
@requires_sign_in()
def my_offers():
    offers = Offer.query.filter_by(owner_id=session['user_id'])
    return render_template('offer/my.html', offers=offers)

@mod_offer.route('/delete/<int:offer_id>', methods=['POST'])
def delete(offer_id):
    offer = Offer.query.get(offer_id)
    if offer.owner_id != session['user_id']:
        return 403
    db.session.delete(offer)
    db.session.commit()
    flash("Usunięto ofertę")
    return redirect(url_for('offer.my_offers'))

@mod_offer.route('/edit/<int:offer_id>', methods=['GET'])
@requires_sign_in()
def edit(offer_id):
    offer = Offer.query.get(offer_id)
    if offer.owner_id != session['user_id']:
        return 403
    return render_template('offer/edit.html', offer=offer)

@mod_offer.route('/edit/<int:offer_id>', methods=['POST'])
@requires_sign_in()
def edit_post(offer_id):
    offer = Offer.query.get(offer_id)
    if offer.owner_id != session['user_id']:
        return 403
    offer.city = request.form['city']
    offer.street = request.form['street']
    offer.building_number = request.form['building_number']
    offer.apartment_number = int(request.form['apartment_number'])
    offer.room_count = int(request.form['room_count'])
    offer.area = int(request.form['area'])
    offer.tier = int(request.form['tier'])
    offer.has_balcony = 'has_balcony' in request.form and request.form['has_balcony'] == 'on'
    offer.description = request.form['description']
    offer.price = int(request.form['price'])
    offer.owner_id = session['user_id']
    offer.utc_publish_date = datetime.datetime.now()
    offer.is_sold = False

    validator = OfferValidator(lambda: offer)

    errors, valid = validator.validate()
    if not valid:
        for e in errors:
            flash(e.message)
        return redirect(url_for('offer.edit', offer_id=offer.id))

    db.session.commit()
    flash("Zaktualizowano ogłoszenie")

    return redirect(url_for("offer.show_offer", offer_id=offer.id))


@mod_offer.route('/search/', methods=['GET'])
def search():
    params = request.args.to_dict()

    query = Offer.query

    filters = [
        CreateFilter('room_count', 'liczba pokoi', lambda: params, Offer.room_count)
    ]

    validators = CombinedValidator(filters)

    errors, valid = validators.validate()
    if not valid:
        for e in errors:
            flash(e.message, 'errorflash')
            return render_template('offer/search.html', params=params)

    for filter in filters:
        query = filter.filter(query)

    results = query.all()
    return render_template('offer/search.html', offers=results, params=params)
