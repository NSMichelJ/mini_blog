from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms.validators import DataRequired
from wtforms.validators import EqualTo
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import Length

from app.common.form import BaseUserForm

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
        Length(min=8)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        Length(min=8),
        EqualTo('password')
    ])