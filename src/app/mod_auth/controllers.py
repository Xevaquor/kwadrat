from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

from app import db

from app.mod_auth.forms import LoginForm
from app.mod_auth.models import User

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():
	pass