from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RegistrationForm,  LoginForm
from app import db
from app.models import User
import sys

@app.route('/')
@login_required
def index():
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    # Authenticated users are redirected to home page.
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # Query DB for user by username
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user is None:
            return render_template('login.html', form=form, user_not_found=True) 
        if user.active:
            if user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                return render_template('login.html', form=form, wrong_pass=True)    
        else:
            return render_template('login.html', form=form, not_active=True) 
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#def is_admin():
    '''
   # Helper function to determine if authenticated user is an admin.
    '''
    #if current_user:
        #if current_user.type == 'admin':   #Elvis Edit changed from user.role to user.type may have to switch back
       #     return True
        #else:
           # return False
   # else:
    #    print('User not authenticated.', file=sys.stderr)


@app.route('/sign_up', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Extract values from form
       # user = User(first_name=form.first_name.data,last_name=form.last_name.data,email=form.email.data,address=form.address.data,gender=form.gender.data)
       # user.set_password(form.password.data)
        firstname = form.first_name.data
        lastname = form.last_name.data
        email = form.email.data
        address = form.address.data
        gender = form.gender.data
        major_id= form.major_id.data
        if  form.validate_email(email)== False:
            return render_template('register.html', title='SignUp', form=form, user_exists=True)
        
        # Create a  record to store in the DB
        u = User(first_name=firstname, last_name=lastname,email=email,address=address,gender=gender,major_id=major_id,active=True,user_type='user' )
        u.set_password(form.password.data)
        # add record to table and commit changes
        db.session.add(u)
        db.session.commit()

        login_user(u)
        return redirect(url_for('index'))
    return render_template('register.html', title='SignUp', form=form)





@app.route('/view_profilepage')
def view():
    print(all, file=sys.stderr)
    return render_template('profilepage.html')


