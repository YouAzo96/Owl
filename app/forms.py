from flask_wtf import FlaskForm
from wtforms import StringField,SelectField, IntegerField, SubmitField, TextField, PasswordField, BooleanField,FileField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, Major

class RegistrationForm(FlaskForm):
    first_name = StringField('FirstName', validators= [DataRequired()], render_kw={"placeholder": "First Name"})
    last_name = StringField('LastName', validators= [DataRequired()], render_kw={"placeholder": "Last Name"})
    image= FileField()
    email = StringField('Email', validators= [DataRequired(), Email()], render_kw={"placeholder": "Email", "id":"email1"})
    address = StringField('Address', validators= [DataRequired()], render_kw={"placeholder": "Address"})
    gender = StringField('Gender', validators= [DataRequired()], render_kw={"placeholder": "Gender"})
    major_id= SelectField('Major', validators= [DataRequired()], render_kw={"placeholder": "Major"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password", "id":"pass"})
    password2= PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Verify Password"})
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
