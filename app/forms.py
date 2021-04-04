from flask_wtf import FlaskForm
from wtforms import StringField,SelectField, IntegerField, SubmitField, TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, Major

class RegistrationForm(FlaskForm):
    first_name = StringField('FirstName', validators= [DataRequired()])
    last_name = StringField('LastName', validators= [DataRequired()])
    email = StringField('Email', validators= [DataRequired(), Email()])
    address = StringField('Address', validators= [DataRequired()])
    gender = StringField('Gender', validators= [DataRequired()])
    major_id= SelectField('Major', validators= [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2= PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_email(self,email):
        user= User.query.filter_by(email=self.email.data).first()
        if user is not None:
            return False
    def __init__(self, *args,**kwargs):
        super(RegistrationForm, self).__init__(*args,**kwargs)
        self.major_id.choices=[(c.major_id,c.major_name) for c in Major.query.all()]


class LoginForm(FlaskForm):
    email = TextField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
