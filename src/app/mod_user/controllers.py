from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort

from app import db
from app.model.offer import Offer

from app.model.user import User, Message

from app.pass_utils import PasswordUtil

from app.model.validator import *

from app.mod_auth.autorization_required import requires_sign_in, requires_not_signed_in, get_unread_messages_count, \
    requires_admin

mod_user = Blueprint('user', __name__, url_prefix='/user')


def sign_in_user(login, password):
    user = User.query.filter_by(email=login).first()
    if user is None: return False
    pu = PasswordUtil()
    hashed_password = pu.hash_password(password, user.salt)
    return hashed_password == user.password


@mod_user.route('/', methods=['GET'])
@requires_admin()
def index():
    users = User.query.all()
    return render_template('user/index.html', users=users)


@mod_user.route('/<int:id>', methods=['GET'])
@requires_admin()
def get(id):
    user = User.query.get(id)
    if user is None:
        abort(404)
    else:
        return render_template('user/details.html', user=user)


@mod_user.route('/delete/<int:id>', methods=['POST'])
@requires_admin()
def delete(id):
    user = User.query.get(id)
    if user is None:
        abort(404)
    if user.is_admin:
        flash("Nie można usunąć adnimistratora")
        return redirect(url_for('user.index'))
    else:
        messages_sent = Message.query.filter_by(from_id=user.id).delete()
        messages_recv = Message.query.filter_by(to_id=user.id).delete()
        offers = Offer.query.filter_by(owner_id=user.id)
        for o in offers:
            for p in o.photos:
                db.session.delete(p)
            Message.query.filter_by(offer_id=o.id).delete()
            db.session.delete(o)
        db.session.delete(user)
        db.session.commit()
        flash('Usunięto użytkownika ' + user.email)
        return redirect(url_for('user.index'))


@mod_user.route('/password/<int:id>', methods=['POST'])
@requires_admin()
def set_password(id):
    password = request.form["password"]
    password_confirmation = request.form["password_confirmation"]

    pv = PasswordValidator(lambda: password, lambda: password_confirmation)
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
@requires_not_signed_in()
def sign_up():
    return render_template('user/sign_up.html')


@mod_user.route('/signup', methods=['POST'])
@requires_not_signed_in()
def create():
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']
    password_confirmation = request.form['password_confirmation']

    validator = CombinedValidator(validators=[
        EmailValidator(lambda: email),
        PasswordValidator(lambda: password, lambda: password_confirmation),
        PhoneValidator(lambda: phone),
        UniqueEmailValidator(lambda: email)
    ])

    errors, valid = validator.validate()
    if not valid:
        for e in errors:
            flash(e.message)
        return redirect(url_for('user.sign_up'))

    pu = PasswordUtil()
    user = User()
    user.email = email
    user.phone = phone
    user.salt = pu.generate_salt()
    user.password = pu.hash_password(password, user.salt)
    user.is_admin = False

    db.session.add(user)
    db.session.commit()

    flash('Możesz się teraz zalogować')
    return redirect(url_for('user.sign_in'))


@mod_user.route('/signin', methods=['GET'])
@requires_not_signed_in()
def sign_in():
    return render_template('user/sign_in.html')


@mod_user.route('/signin', methods=['POST'])
@requires_not_signed_in()
def sign_in_post():
    email = request.form['email']
    password = request.form['password']
    signed_in = sign_in_user(email, password)
    if signed_in:
        flash('Zalogowano jako ' + email)
        session['username'] = email
        session['user_id'] = User.query.filter_by(email=email).first().id
        session['unread_messages'] = get_unread_messages_count()
        session['is_admin'] = User.query.filter_by(email=email).first().is_admin
        # if 'next_url' in session and not session['is_admin']:
        #     next_url = session['next_url']
        #     del session['next_url']
        #     return redirect(next_url, code=307)
        # else:
        return redirect(url_for('index'))
    else:
        flash('Niepoprawy email i/lub hasło', 'alert-warning')
        return redirect(url_for('user.sign_in'), code=303)



@mod_user.route('/signout', methods=['POST'])
def sign_out():
    if 'username' in session:
        del session['username']
        del session['user_id']
        del session['is_admin']
        del session['unread_messages']
        if 'recent' in session: del session['recent']
    flash('Wylogowano')
    return redirect(url_for('index'))


@mod_user.route('/admin/', methods=['GET'])
@requires_admin()
def admin_index():
    return render_template('user/admin.html')

@mod_user.route('/report', methods=['GET'])
@requires_admin()
def report():
    month = 0
    year = 0
    try:
        s = request.args['month'].split('-')
        month = int(s[1])
        year = int(s[0])

        if not(( 0 < month <= 12) and (1900 < year < 2035)):
            raise Exception()

    except:
        flash("Nieporawna data", "alert-danger")
        return redirect(url_for('user.admin_index'))

    offers = Offer.query.filter_by(is_sold=True).all()

    price = 0
    area = 0
    oc = 0
    for o in offers:
        if o.sold_date.year == year and o.sold_date.month == month:
            price += o.price
            area += o.area
            oc += 1

    if oc == 0:
        flash("Nie sprzedano zadnych mieszkań w tym miesiącu :(", "alert-danger")
        return redirect(url_for('user.admin_index'))

    return render_template('user/report.html', count=oc,
                           avg_price=price/oc,
                           avg_area=area/oc,
                           month=request.args['month'])


