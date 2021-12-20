from functools import wraps

from flask import redirect
from flask import url_for
from flask_login import current_user

# Decorador para redirigir al usuario
# A una ulr pasada como parametro
# Si el usuario ya esta autenticado
def if_user_authenticated_redirect(redirect_to):
    def decorate_function(function):
        @wraps(function)
        def wrapper(*args, **kws):
            if current_user.is_authenticated:
                return redirect(url_for(redirect_to))
            return function(*args, **kws)
        return wrapper
    return decorate_function