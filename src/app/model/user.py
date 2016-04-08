from app import db



class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean, nullable=False)
    email = db.Column(db.Unicode(256), nullable=False, unique=True)
    phone = db.Column(db.Unicode(12), nullable=False)
    password = db.Column(db.Unicode(64), nullable=False)
    salt = db.Column(db.Unicode(255), nullable=False)
    offers = db.relationship('Offer', backref='user', lazy='dynamic')
    sent_messages = db.relationship('Message', backref='from', lazy='dynamic', foreign_keys="Message.from_id")
    received_messages = db.relationship('Message', backref='to', lazy='dynamic', foreign_keys="Message.to_id")


    def __init__(self, email, phone, password):
        self.email = email
        self.phone = phone
        self.password = 'asdf'  # do the magic here
        self.is_admin = False
        self.salt = 'xd'

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.UnicodeText, nullable=False)
    is_read = db.Column(db.Boolean, nullable=False)

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




