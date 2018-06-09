from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    uploaded_file = FileField('Upload a *.txt file:', validators=[FileAllowed(['txt']), DataRequired()])    
    submit = SubmitField('Post')
