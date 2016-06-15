import app
from app.model.user import User, Message
from app.model.offer import Offer, Photo
from faker import Factory
from app.pass_utils import PasswordUtil
import random
import datetime
import dateutil
import sys
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

fake = Factory.create('pl_PL')

AMOUNT_OF_USERS = 50
AMOUNT_OF_MESSAGES = 180
AMOUNT_OF_OFFERS = 100

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
    print('.', end='')

app.db.session.commit()

admin = User()
admin.email = 'admin@admin.pl'
admin.is_admin = True
admin.salt = pu.generate_salt()
admin.password = pu.hash_password('admin', admin.salt)
admin.phone = '123654789'

app.db.session.add(admin)
app.db.session.commit()

p = User()
p.email = 'p@p.pl'
p.is_admin = False
p.salt = pu.generate_salt()
p.password = pu.hash_password('ppp', p.salt)
p.phone = '123654789'

app.db.session.add(p)
app.db.session.commit()

a = User()
a.email = 'a@a.pl'
a.is_admin = False
a.salt = pu.generate_salt()
a.password = pu.hash_password('aaa', a.salt)
a.phone = '123654789'

app.db.session.add(a)
app.db.session.commit()

for _ in range(AMOUNT_OF_OFFERS):
    offer = Offer()
    offer.apartment_number = random.randint(1, 500) if random.choice([True, False]) else None
    offer.area = random.randint(20, 120)
    offer.building_number = random.choice(['1', '18c', '7', '48d', '32' '184', '234', '784', '42u'])
    offer.city = fake.city()
    offer.description = fake.paragraph()
    offer.has_balcony = random.choice([True, False])
    # TODO:
    offer.is_sold = fake.boolean()
    offer.sold_date = datetime.datetime.now() if offer.is_sold else None
    offer.owner_id = random.randint(1, AMOUNT_OF_USERS)
    offer.price = random.randint(1e5, 1e7)
    offer.room_count = random.randint(1, 7)
    offer.street = fake.street_name()
    offer.tier = random.randint(0, 3)
    offer.publish_date = datetime.datetime.now()

    app.db.session.add(offer)
    app.db.session.commit()

    p1 = Photo()
    p1.filename = random.sample(['a.png', 'b.png', 'c.png'], 1)[0]
    p1.offer_id = offer.id
    p2 = Photo()
    p2.filename = random.sample(['a.png', 'b.png', 'c.png'], 1)[0]
    p2.offer_id = offer.id
    app.db.session.add(p1)
    app.db.session.add(p2)
    print('.', end='')


app.db.session.commit()

for _ in range(AMOUNT_OF_MESSAGES):
    msg = Message()
    msg.from_id = random.randint(1, AMOUNT_OF_USERS)
    offset = random.randint(1, AMOUNT_OF_USERS - 1)
    msg.to_id = p.id if _ % 10 == 0 else (msg.from_id + offset) % AMOUNT_OF_USERS + 1
    msg.is_read = random.randint(0, 1) % 2 == 0
    print(msg.to_id, p.id, msg.is_read)
    msg.content = fake.paragraph()
    msg.sent_datetime = datetime.datetime.now()
    msg.offer_id = random.sample(range(AMOUNT_OF_OFFERS - 1), 1)[0] + 1

    app.db.session.add(msg)
    print('.', end='')


app.db.session.commit()
results = Offer.query.filter_by(building_number=1).all()
print('asd')
