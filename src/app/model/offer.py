from app import db


class Offer(db.Model):
    __tablename__ = 'offer'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    city = db.Column(db.Unicode(64), nullable=False)
    street = db.Column(db.Unicode(128), nullable=False)
    # TODO:
    building_number = db.Column(db.String(5), nullable=False)
    apartment_number = db.Column(db.Integer, nullable=True)
    room_count = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Integer, nullable=False)
    tier = db.Column(db.Integer, nullable=False)
    has_balcony = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.Unicode(16 * 1024), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    publish_date = db.Column(db.DateTime, nullable=False)
    sold_date = db.Column(db.DateTime, nullable=True)
    is_sold = db.Column(db.Boolean, nullable=False)

    photos = db.relationship('Photo', backref='from', lazy='dynamic', foreign_keys="Photo.offer_id",
                                    cascade='save-update, merge, delete')

    @staticmethod
    def Create(owner_id, city, street, house_number, apartment_number, room_count,
               area, tier_count, has_balcony, description, price):
        pass


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, nullable=False)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'), index=True, nullable=False)
