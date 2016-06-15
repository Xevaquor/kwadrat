from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, IntegerField, BooleanField
from wtforms.validators import Required


# city = db.Column(db.Unicode(64), nullable=False)
#     street = db.Column(db.Unicode(128), nullable=False)
#     house_number = db.Column(db.Integer, nullable=False)
#     apartment_number = db.Column(db.Integer, nullable=True)
#     room_count = db.Column(db.Integer, nullable=False)
#     area = db.Column(db.Integer, nullable=False)
#     tier_count = db.Column(db.Integer, nullable=False)
#     has_balcony = db.Column(db.Boolean, nullable=False)
#     description = db.Column(db.Unicode(16 * 1024), nullable=False)
#     price = db.Column(db.Integer, nullable=False)
#
#     publish_date = db.Column(db.Date, nullable=False)
#     sold_date = db.Column(db.Date, nullable=True)
#     is_sold = db.Column(db.Boolean, nullable=False)

class CreateOfferForm(Form):
    street = StringField('street')
    house_number = IntegerField('house_number')
    apartment_number = IntegerField('apartment_number')
    room_count = IntegerField('room_count')
    area = IntegerField('area')
    tier_count = IntegerField('tier_count')
    has_balcony = BooleanField('has_balcony', default=False)
    description = TextAreaField('description')
    price = IntegerField('price')


