from flask_wtf import Form
from wtforms import StringField

class MusicForm(Form):
    name = StringField('name')
