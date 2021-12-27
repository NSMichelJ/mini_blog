import re

from flask_login import current_user
from wtforms.validators import ValidationError

from app.auth.models import User

class IsUsernameBusy(object):
    """
    Verifica si el username esta ocupado
    """
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        self.user = User.query.filter_by(username=field.data).first()
        if self.user is not None:
            if not current_user.is_authenticated or self.user.username != current_user.username:
                if not self.message:
                    message = field.gettext('El nombre de usuario se encuentra\
                    ocupado, por favor elija otro.')
                field.data = ''
                raise ValidationError(message)

class IsEmailBusy(object):
    """
    Verifica si el email esta ocupado
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        user = User.query.filter_by(email=field.data).first()
        if user is not None:
            if not current_user.is_authenticated or user.email != current_user.email:
                if not self.message:
                    message = field.gettext('La dirección de correo electrónico \
                    se encuentra en uso, por favor elija otro.')
                field.data = ''
                raise ValidationError(message)

class UsernameIsalnum(object):
    """
    Verifica si todos los caracteres de la cadena son alfanuméricos
    y hay al menos, un carácter.
    """
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if field.data.isalnum()==False:
            if not self.message:
                message = field.gettext('El nombre de usuario debe contener solo letras o numeros.')
            raise ValidationError(message)

class Password(object):
    """
    Verifica si la contaseña es sugura
    """
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field, message=None):

        regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&.,])[A-Za-z\d@$!#%*?&.,]{8,20}$"
        self.regex = re.compile(regex, 0)

        match = self.regex.match(field.data or "")
        if match:
            return match

        if message is None:
            if self.message is None:
                msg = """La contraseña es insegura, debe contener:
                carácteres en mayúscula y en minúscula, 
                al menos un número,
                un símbolo especial, 
                y una longitud de entre 8 y 20 caracteres."""
                message = field.gettext(msg)
            else:
                message = self.message

        raise ValidationError(message)
