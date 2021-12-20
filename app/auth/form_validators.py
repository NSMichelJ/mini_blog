from wtforms.validators import ValidationError

from .models import User

def validate_username(form, field):
    user = User.query.filter_by(username=field.data).first()
    if user is not None:
        field.data = ''
        raise ValidationError('El usuario esta ocupado, por favor elija otro.')

def validate_email(form, field):
    user = User.query.filter_by(email=field.data).first()
    if user is not None:
        field.data = ''
        raise ValidationError('El email esta ocupado, por favor elija otro.')