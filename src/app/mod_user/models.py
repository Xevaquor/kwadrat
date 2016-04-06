from app import db

class User(db.Model):

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	is_admin = db.Column(db.Boolean, nullable=False)
	email = db.Column(db.Unicode(256), nullable=False, unique=True)
	phone = db.Column(db.Unicode(12), nullable=False)
	password = db.Column(db.Unicode(64), nullable=False)
	salt = db.Column(db.Unicode(16), nullable=False)
	
	def __init__(self, email, phone, password):
		self.email = email
		self.phone = phone
		self.password = 'asdf' # do the magic here
	

# CREATE TABLE Users
# (
    # Id SERIAL PRIMARY KEY NOT NULL,
    # IsAdmin BOOLEAN DEFAULT FALSE NOT NULL,
    # Email VARCHAR(64) NOT NULL,
    # Phone VARCHAR(12) NOT NULL, --883 598 242 +48
    # Password CHAR(64) NOT NULL
# );
# CREATE UNIQUE INDEX users_email_uindex ON Users (Email);
