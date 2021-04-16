
from flask_wtf import FlaskForm
from wtforms import validators, StringField,SelectField, IntegerField,TextAreaField, SubmitField, TextField, PasswordField, BooleanField,FileField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, Major
from wtforms_components  import DateField, TimeField
from flask_wtf.html5 import IntegerRangeField

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

class BanForm(FlaskForm):
    user_id = StringField('User ID: ', validators=[DataRequired()])
    submit = SubmitField('Ban User')


class AddAnnouncement(FlaskForm):
    flag = SelectField('Flag: ',choices=[('Warning!','Warning!'),('Notice','Notice'),('Alert','Alert')], validators=[validators.optional()])
    description = TextAreaField('Description: ', validators=[DataRequired(),validators.length(max=100)])
    submit = SubmitField('Post')

class SchedulerForm(FlaskForm):
    
    
    to_location =  StringField('To Location', validators= [DataRequired()], render_kw={"placeholder": "To location"})
    from_location = StringField('from Location', validators= [DataRequired()], render_kw={"placeholder": "From Location"})
    start_date=  DateField('Start Date' , format = '%Y-%m-%d', validators= [DataRequired()]) 
    end_date=    DateField('End Date' , format = '%Y-%m-%d',validators= [DataRequired()] )
    start_time=  TimeField ('Start Time',validators= [DataRequired()])
    end_time=   TimeField ('End Time',validators= [DataRequired()])
    max_passengers= IntegerRangeField ('Passengers', render_kw={"min":"1", "max": "7","value":"1"})
     
    submit = SubmitField('Submit')

