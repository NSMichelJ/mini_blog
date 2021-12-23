from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms.validators import DataRequired
from wtforms.validators import EqualTo
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import Length
from wtforms.validators import Regexp

from app.common.form import BaseUserForm
from app.common.form.form_validators import regex_valid_password

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    remember_me = BooleanField('Remember me')

class SignupForm(BaseUserForm):
    password = PasswordField('Password', validators=[
        DataRequired(),
        Regexp(regex=regex_valid_password),
        Length(min=8)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        Length(min=8),
        EqualTo('password')
    ])