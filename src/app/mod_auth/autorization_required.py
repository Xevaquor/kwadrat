from functools import wraps, update_wrapper

from flask import session, url_for, redirect, flash, request, abort

from app.model.user import Message, User


def get_unread_messages_count():
    if session['user_id'] is None:
        return 0

    msgs = Message.query.filter_by(to_id=session['user_id'], is_read=False).all()

    if msgs is None:
        return  0

    return len(msgs)

def requires_sign_in():
    def decorator(func):
        def authenticated(*args, **kwargs):
            if 'username' in session:
                session['unread_messages'] = get_unread_messages_count()
                return func(*args, **kwargs)
            flash('Nie jesteś zalogowany')
            session['next_url'] = request.url
            return redirect(url_for('user.sign_in'))

        return update_wrapper(authenticated, func)

    return decorator

def requires_admin():
    def decorator(func):
        def authenticated(*args, **kwargs):
            if 'username' in session and User.query.get(session['user_id']).is_admin:
                session['unread_messages'] = get_unread_messages_count()
                return func(*args, **kwargs)
            flash('Musisz być administratorem')
            session['next_url'] = request.url
            abort(403)

        return update_wrapper(authenticated, func)

    return decorator


def requires_not_signed_in():
    def decorator(func):
        def not_authenticated(*args, **kwargs):
            if 'username' not in session:
                return func(*args, **kwargs)
            flash('Najpierw musisz się wylogować')
            return redirect(url_for('index'))

        return update_wrapper(not_authenticated, func)

    return decorator
