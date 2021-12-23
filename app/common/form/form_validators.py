from flask_login import current_user
from wtforms.validators import ValidationError

from app.auth.models import User

def is_username_busy(form, field):
    """
    Verifica si el usuario esta ocupado
    """
    user = User.query.filter_by(username=field.data).first()
    if user is not None:
        if not current_user.is_authenticated or user.username != current_user.username:
            field.data = ''
            raise ValidationError('El nombre de usuario se encuentra ocupado, por favor elija otro.')
                
def username_isalnum(form, field):
    """
    Verifica si todos los caracteres de la cadena son alfanuméricos
    y hay al menos, un carácter.
    """
    if field.data.isalnum()==False:
        raise ValidationError('El nombre de usuario debe contener solo letras o numeros.')

def is_email_busy(form, field):
    """
    Verifica si el email esta ocupado
    """
    user = User.query.filter_by(email=field.data).first()
    if user is not None:
        if not current_user.is_authenticated or user.email != current_user.email:
            field.data = ''
            raise ValidationError('La dirección de correo electrónico se encuentra en uso, por favor elija otro.')

regex_valid_password = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&.,])[A-Za-z\d@$!#%*?&.,]{8,20}$"
