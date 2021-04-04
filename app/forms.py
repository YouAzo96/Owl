from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField,TextAreaField, SelectField
from wtforms.validators import DataRequired
from wtforms import validators

class AddAnnouncement(FlaskForm):
    flag = SelectField('Flag: ',choices=[('Warning!','Warning!'),('Notice','Notice'),('Alert','Alert')], validators=[validators.optional()])
    description = TextAreaField('Description: ', validators=[DataRequired(),validators.length(max=100)])
    submit = SubmitField('Post')
