from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import IntegerField
from wtforms.validators import DataRequired
from wtforms.validators import NumberRange

class WritePost(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired()
    ])
    content = CKEditorField('Content', validators=[
        DataRequired()
    ])
    read_time = IntegerField('Read time', default=1, validators=[
        NumberRange(min=1)
    ])
