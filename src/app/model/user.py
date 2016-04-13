from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean, nullable=False)
    email = db.Column(db.Unicode(256), nullable=False, unique=True)
    # TODO:
    phone = db.Column(db.Unicode(12), nullable=False)
    password = db.Column(db.Unicode(64), nullable=False)
    salt = db.Column(db.Unicode(255), nullable=False)
    offers = db.relationship('Offer', backref='user', lazy='dynamic')
    sent_messages = db.relationship('Message', backref='from', lazy='dynamic', foreign_keys="Message.from_id")
    received_messages = db.relationship('Message', backref='to', lazy='dynamic', foreign_keys="Message.to_id")


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.UnicodeText, nullable=False)
    is_read = db.Column(db.Boolean, nullable=False)
    sent_datetime = db.Column(db.DateTime, nullable=False)

    @staticmethod
    def Create(from_id, to_id, content):
        msg = Message()
        msg.from_id = from_id
        msg.to_id = to_id
        msg.content = content
        msg.is_read = False