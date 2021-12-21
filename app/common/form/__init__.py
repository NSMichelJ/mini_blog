from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import Length

from .form_validators import *

class BaseUserForm(FlaskForm):
    """
    Formulario base para el SignupForm y el EditProfileForm
    """
    username = StringField('Username', validators=[
        DataRequired('Es necesario que rellene este campo'),
        is_username_busy,
        Length(min=6, max=12),
        username_isalnum
    ])
    first_name = StringField('First Name', validators=[
        Length(min=3, max=12),
        DataRequired('Es necesario que rellene este campo')
    ])
    last_name = StringField('Last Name', validators=[
        Length(min=3, max=12),
        DataRequired('Es necesario que rellene este campo'),
    ])
    email = StringField('Email', validators=[
        DataRequired('Es necesario que rellene este campo'),
        Email('La dirección de corre electrónico no es correcta'),
        is_email_busy
    ])
