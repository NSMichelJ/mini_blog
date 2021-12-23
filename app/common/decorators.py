from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user

def check_confirmed(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.confirmed is False:
            flash('Por favor confirma tu email!', 'warning')
            return redirect(url_for('auth.unconfirmed'))
        return function(*args, **kwargs)
    return wrapper