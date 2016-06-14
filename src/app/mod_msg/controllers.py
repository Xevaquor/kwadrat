import datetime

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, session, abort

from app.mod_auth.autorization_required import requires_sign_in, get_unread_messages_count

from app.model.user import User, Message
from app.model.offer import Offer

from app import db

mod_msg = Blueprint('msg', __name__, url_prefix='/message')


def is_logged_in_as_specific_user_id(expected_id):
    if 'username' not in session:
        return False
    username = session['username']
    actual_id = User.query.filter_by(email=username).first().id
    return actual_id == expected_id


@mod_msg.route('/', methods=['GET'])
@requires_sign_in()
def index():
    msgs = Message.query.filter_by(to_id=session['user_id'])
    return render_template('msg/index.html', messages=list(msgs))


@mod_msg.route('/<int:id>', methods=['GET'])
@requires_sign_in()
def show(id):
    msg = Message.query.get(id)
    if msg is None:
        abort(404)
    if not is_logged_in_as_specific_user_id(msg.to_id):
        abort(403)
    msg.is_read = True
    db.session.commit()

    session['unread_messages'] = get_unread_messages_count()

    return render_template('msg/details.html', message=msg)

@mod_msg.route('/delete/<int:id>', methods=['POST'])
@requires_sign_in()
def delete(id):
    msg = Message.query.get(id)
    if msg is None:
        abort(404)
    if not is_logged_in_as_specific_user_id(msg.to_id):
        abort(403)
    db.session.delete(msg)
    db.session.commit()
    flash('Usunięto wiadomość')
    return redirect(url_for('msg.index'))

@mod_msg.route('/want_buy/<int:offer_id>', methods=['POST'])
@requires_sign_in()
def want_buy(offer_id):
    offer = Offer.query.get(offer_id)
    if offer is None:
        abort(404)
    if is_logged_in_as_specific_user_id(offer.owner_id):
        flash("Nie możesz kupić własnego mieszkania!")
        abort(403)
    msg = Message()
    msg.from_id = session['user_id']
    msg.is_read = False
    msg.sent_datetime = datetime.datetime.now()
    msg.to_id = offer.owner_id
    msg.offer_id = offer_id

    db.session.add(msg)
    db.session.commit()

    flash("Zgłoszono chęć zakupu")
    return redirect(url_for('offer.show_offer', offer_id=offer.id))\

