from app import db


class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    city = db.Column(db.Unicode(64), nullable=False)
    street = db.Column(db.Unicode(128), nullable=False)
    house_number = db.Column(db.Integer, nullable=False)
    apartment_number = db.Column(db.Integer, nullable=True)
    room_count = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Integer, nullable=False)
    tier_count = db.Column(db.Integer, nullable=False)
    has_balcony = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.Unicode(16 * 1024), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    utc_publish_date = db.Column(db.Date, nullable=False)
    utc_sold_date = db.Column(db.Date, nullable=True)
    is_sold = db.Column(db.Boolean, nullable=False)

    @staticmethod
    def Create(owner_id, city, street, house_number, apartment_number, room_count,
               area, tier_count, has_balcony, description, price):
        pass
