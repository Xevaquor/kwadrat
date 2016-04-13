import app
from app.model.user import User, Message

app.db.drop_all()
app.db.create_all()

print(app.db)

jarek = User('jarek@pis.pl', '874135845', 'kod')
duda = User('andżej@pis.pl', '789654123', 'asdf')

app.db.session.add(jarek)
app.db.session.add(duda)

app.db.session.commit()

msg = Message()
msg.content = 'elo zią'
msg.from_id = jarek.id
msg.to_id = duda.id
msg.is_read = False

app.db.session.add(msg)

app.db.session.commit()


