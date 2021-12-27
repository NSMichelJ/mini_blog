from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, Length

from app.common.form import BaseUserForm
from app.common.form.form_validators import Password

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
        Password(),
        Length(min=8, max=20)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired('Es necesario que rellene este campo'),
        Length(min=8, max=20),
        EqualTo('password', message='La contraseñas deben ser iguales')
    ])

class SignupForm(BaseUserForm, BasePasswordForm):
    pass

class ResetPasswordForm(FlaskForm, BasePasswordForm):
    email = StringField('Email', validators=[
        DataRequired('Es necesario que rellene este campo'),
        Email('La dirección de corre electrónico no es correcta'),
    ])
