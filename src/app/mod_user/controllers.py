from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

from app import db

from app.mod_user.models import User

mod_user = Blueprint('user', __name__, url_prefix='/user')

@mod_user.route('/', methods=['GET'])
def index():
	return render_template('user/index.html')
