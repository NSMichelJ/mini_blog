from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, IntegerField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, \
                NumberRange, Optional

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
