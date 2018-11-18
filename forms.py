from flask_wtf import FlaskForm
from wtforms import StringField

class MusicForm(FlaskForm):
    name = StringField('name')
