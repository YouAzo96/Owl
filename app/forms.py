from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextField, PasswordField
from wtforms.validators import DataRequired

class AddUser(FlaskForm):
    user_id = StringField('Username:', validators=[DataRequired()])
    first_name = StringField('FirstName', validators= [DataRequired()])
    last_name = StringField('LastName', validators= [DataRequired()])
    email = StringField('Email', validators= [DataRequired()])
    address = StringField('Address', validators= [DataRequired()])
    gender = StringField('Gender', validators= [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Save')

class SelectUserForm(FlaskForm):
    user = StringField('Username:', validators=[DataRequired()])
    submit = SubmitField('Block')


class LoginForm(FlaskForm):
    user = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
