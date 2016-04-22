from functools import wraps, update_wrapper

from flask import session, url_for, redirect, flash, request


def requires_sign_in():
    def decorator(func):
        def authenticated(*args, **kwargs):
            if 'username' in session:
                return func(*args, **kwargs)
            flash('Nie jesteś zalogowany')
            session['next_url'] = request.url
            return redirect(url_for('user.sign_in'))

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
