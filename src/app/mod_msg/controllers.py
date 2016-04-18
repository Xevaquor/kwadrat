from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, session, abort

from app.mod_auth.autorization_required import requires_sign_in

from app.model.user import User, Message

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
    user = User.query.filter_by(email=session['username']).first()
    msgs = user.received_messages.order_by(Message.sent_datetime.desc())
    return render_template('msg/index.html', messages=msgs)


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
