from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms.validators import DataRequired
from wtforms.validators import EqualTo
from wtforms.validators import Email

from .form_validators import validate_username, validate_email

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    remember_me = BooleanField('Remember me')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        validate_username
    ])
    first_name = StringField('First Name', validators=[
        DataRequired()
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired()
    ])
    email = email = StringField('Email', validators=[
        DataRequired('Este campo es necesario'),
        Email('La direccion de email es invalida'),
        validate_email
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password')
    ])