from functools import wraps

from flask import abort
from flask_login import current_user

# Decorador para verificar
# Si el usuario es admin
def admin_required(function):
    @wraps(function)
    def wrapper(*args, **kws):
        if not current_user.is_admin():
            abort(401)
        return function(*args, **kws)
    return wrapper
