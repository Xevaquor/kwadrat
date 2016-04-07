from flask import Flask, render_template
import flask.ext.sqlalchemy

app = Flask(__name__)
app.config.from_object('config')

db = flask.ext.sqlalchemy.SQLAlchemy(app)

@app.errorhandler(404)
def not_found(error):
	return '404 not found'

#from app.asdf import asdf
#from app.mod_user.controllers import mod_user as user_module

#app.register_blueprint(user_module)
