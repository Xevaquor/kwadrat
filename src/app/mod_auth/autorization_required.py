from functools import wraps, update_wrapper

from flask import session, url_for, redirect, flash


def requires_sign_in():
    def decorator(func):
        def authenticated(*args, **kwargs):
            if 'username' in session:
                return func(*args, **kwargs)
            flash('Nie jesteś zalogowany')
            return redirect(url_for('auth.signin'))
        return update_wrapper(authenticated, func)
    return decorator
