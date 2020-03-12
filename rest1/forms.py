from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class MainForm(FlaskForm):
    pokemon1_name = StringField('First pokemon name')
    pokemon1_level = StringField('First pokemon level')
    pokemon2_name = StringField('Second pokemon name')
    pokemon2_level = StringField('Second pokemon level')
    submit = SubmitField('Who\'s gonna win?')
