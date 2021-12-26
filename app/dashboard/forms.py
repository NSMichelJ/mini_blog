from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField
from wtforms import IntegerField
from wtforms import PasswordField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import NumberRange
from wtforms.validators import EqualTo
from wtforms.validators import Regexp, Optional

from app.common.form import BaseUserForm
from app.common.form.form_validators import Password

class WritePostForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired()
    ])
    content = CKEditorField('Content', validators=[
        DataRequired()
    ])
    read_time = IntegerField('Read time', default=1, validators=[
        NumberRange(min=1)
    ])

class EditProfileForm(BaseUserForm):
    password = PasswordField('Password', validators=[
        Optional(),
        Password(),
        Length(min=8, max=20)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        EqualTo('password'),
    ])
