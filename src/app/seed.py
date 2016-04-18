import app
from app.model.user import User, Message
from app.model.offer import Offer, Photo
from faker import Factory
from app.pass_utils import PasswordUtil
import random
import datetime
import dateutil

# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

fake = Factory.create('pl_PL')

AMOUNT_OF_USERS = 10
AMOUNT_OF_MESSAGES = 20
AMOUNT_OF_OFFERS = 15

pu = PasswordUtil()

app.db.session.commit()
app.db.drop_all()
app.db.create_all()

for _ in range(AMOUNT_OF_USERS):
    user = User()
    user.email = fake.email()
    user.is_admin = False
    user.salt = pu.generate_salt()
    user.password = pu.hash_password(fake.password(), user.salt)
    user.phone = '123654789'

    app.db.session.add(user)

app.db.session.commit()

for _ in range(AMOUNT_OF_MESSAGES):
    msg = Message()
    msg.from_id = random.randint(1, AMOUNT_OF_USERS)
    offset = random.randint(1, AMOUNT_OF_USERS-1)
    msg.to_id = (msg.from_id + offset) % AMOUNT_OF_USERS + 1
    msg.is_read = random.randint(0,1) % 2 == 0
    msg.content = fake.paragraph()
    msg.sent_datetime = datetime.datetime.now()

    app.db.session.add(msg)

app.db.session.commit()

for _ in range(AMOUNT_OF_OFFERS):
    offer = Offer()
    offer.apartment_number = random.randint(1, 500) if random.choice([True, False]) else None
    offer.area = random.randint(20,120)
    offer.building_number = random.choice(['1', '18c'])
    offer.city = fake.city()
    offer.description = fake.paragraph()
    offer.has_balcony = random.choice([True, False])
    # TODO:
    offer.is_sold = fake.boolean()
    offer.utc_sold_date = datetime.datetime.utcnow() if offer.is_sold else None
    offer.owner_id = random.randint(1, AMOUNT_OF_USERS)
    offer.price = random.randint(1e5, 1e7)
    offer.room_count = random.randint(1, 7)
    offer.street = fake.street_name()
    offer.tier_count = random.randint(1,3)
    offer.utc_publish_date = datetime.datetime.now()

    app.db.session.add(offer)

app.db.session.commit()

results = Offer.query.filter_by(building_number=1).all()
print('asd')


