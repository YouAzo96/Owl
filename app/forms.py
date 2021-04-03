from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class RegistrationForm(FlaskForm):
    first_name = StringField('FirstName', validators= [DataRequired()])
    last_name = StringField('LastName', validators= [DataRequired()])
    email = StringField('Email', validators= [DataRequired(), Email()])
    address = StringField('Address', validators= [DataRequired()])
    gender = StringField('Gender', validators= [DataRequired()])
    major_id= StringField('Gender', validators= [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2= PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self,email):
        user= User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address')


class LoginForm(FlaskForm):
    email = TextField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
