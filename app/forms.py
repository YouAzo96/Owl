from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class BanForm(FlaskForm):
    user_id = StringField('User ID: ', validators=[DataRequired()])
    submit = SubmitField('Ban User')


