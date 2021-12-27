from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
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
        Length(min=6, max=12),
        UsernameIsalnum(),
        IsUsernameBusy()
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
        IsEmailBusy()
    ])
    profile_image = FileField('imagen de perfil', validators=[
        FileAllowed(['jpg', 'png'], 'Solo se permiten imágenes')
    ])
    background_image = FileField('Imagen de fondo', validators=[
        FileAllowed(['jpg', 'png'], 'Solo se permiten imágenes')
    ])
