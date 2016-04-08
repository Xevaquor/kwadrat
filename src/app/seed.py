import app
from app.model.user import User

app.db.drop_all()
app.db.create_all()

print(app.db)

jarek = User('jarek@pis.pl', '874135845', 'kod')

app.db.session.add(jarek)
app.db.session.add(jarek)
app.db.session.commit()


