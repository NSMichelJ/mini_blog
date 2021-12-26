from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms.validators import DataRequired
from wtforms.validators import EqualTo
from wtforms.validators import Email
from wtforms.validators import Length
from wtforms.validators import Regexp

from app.common.form import BaseUserForm
from app.common.form.form_validators import regex_valid_password

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired('Es necesario que rellene este campo'),
    ])
    password = PasswordField('Password', validators=[
        DataRequired('Es necesario que rellene este campo'),
    ])
    remember_me = BooleanField('Remember me')

class BasePasswordForm():
    """
    Form base para los campos de contraseñas
    del SignupForm y el ResetPasswordForm
    """
    password = PasswordField('Password', validators=[
        DataRequired('Es necesario que rellene este campo'),
        Regexp(regex=regex_valid_password),
        Length(min=8)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired('Es necesario que rellene este campo'),
        Length(min=8),
        EqualTo('password')
    ])

class SignupForm(BaseUserForm, BasePasswordForm):
    pass

class ResetPasswordForm(FlaskForm, BasePasswordForm):
    email = StringField('Email', validators=[
        DataRequired('Es necesario que rellene este campo'),
        Email('La dirección de corre electrónico no es correcta'),
    ])
