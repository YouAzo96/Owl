from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextField, PasswordField
from wtforms.validators import DataRequired

class AddUser(FlaskForm):
    first_name = StringField('FirstName', validators= [DataRequired()])
    last_name = StringField('LastName', validators= [DataRequired()])
    email = StringField('Email', validators= [DataRequired()])
    address = StringField('Address', validators= [DataRequired()])
    gender = StringField('Gender', validators= [DataRequired()])
    major_id= StringField('Gender', validators= [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Save')


class LoginForm(FlaskForm):
    email = TextField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
