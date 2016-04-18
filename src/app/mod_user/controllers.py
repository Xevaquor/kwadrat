from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort

from app import db

from app.model.user import User

from app.pass_utils import PasswordUtil

from app.model.validator import *

from app.mod_auth.autorization_required import requires_sign_in

mod_user = Blueprint('user', __name__, url_prefix='/user')


@mod_user.route('/', methods=['GET'])
def index():
    users = User.query.all()
    return render_template('user/index.html', users=users)


@mod_user.route('/<int:id>', methods=['GET'])
@requires_sign_in()
def get(id):
    user = User.query.get(id)
    if user is None:
        abort(404)
    else:
        return render_template('user/details.html', user=user)


@mod_user.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    user = User.query.get(id)
    if user is None:
        abort(404)
    else:
        db.session.delete(user)
        db.session.commit()
        flash('Usunięto użytkownika ' + user.email)
        return redirect(url_for('user.index'))


@mod_user.route('/password/<int:id>', methods=['POST'])
def set_password(id):
    password = request.form["password"]
    password_confirmation = request.form["password_confirmation"]

    pv = PasswordValidator(lambda : password, lambda : password_confirmation)
    errors, valid = pv.validate()
    if not valid:
        for e in errors:
            flash(e.message)
        return redirect(url_for('user.get', id=id))

    user = User.query.get(id)
    if user is None:
        abort(404)

    pu = PasswordUtil()
    salt = pu.generate_salt()
    sha = pu.hash_password(password, salt)
    user.salt = salt
    user.password = sha
    db.session.commit()
    flash('Zmieniono')
    return redirect(url_for('user.get', id=id))


@mod_user.route('/signup', methods=['GET'])
def sign_up():
    return render_template('user/sign_up.html')


@mod_user.route('/signup', methods=['POST'])
def sign_up_post():
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']
    password_confirmation = request.form['password_confirmation']

    validator = CombinedValidator(validators=[
        EmailValidator(lambda : email),
        PasswordValidator(lambda : password, lambda : password_confirmation),
        PhoneValidator(lambda : phone)
    ])

    errors, valid = validator.validate()
    if not valid:
        for e in errors:
            flash(e.message)
        return redirect(url_for('user.sign_up'))

    # do magic


@mod_user.route('/signin', methods=['GET'])
def sign_in():
    return render_template('user/sign_in.html')


@mod_user.route('/signin', methods=['POST'])
def sign_in_post():
    return render_template('user/sign_in.html')


@mod_user.route('/signout', methods=['POST'])
def sign_out():
    return redirect(url_for('index'))
