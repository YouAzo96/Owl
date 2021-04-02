from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import AddUser, SelectUserForm, LoginForm
from app import db
from app.models import User
import sys

@app.route('/')
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
        if active:
             if user is None or not user.check_password(form.password.data):
                 print('Login failed', file=sys.stderr)
                 return redirect(url_for('login'))
             # login_user is a flask_login function that starts a session
             login_user(user)
             print('Login successful', file=sys.stderr)
             return redirect(url_for('view'))
        else:
        return render_template('unauthorized_user.html', form=form)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

def is_admin():
    '''
    Helper function to determine if authenticated user is an admin.
    '''
    if current_user:
        if current_user.type == 'admin':   #Elvis Edit changed from user.role to user.type may have to switch back
            return True
        else:
            return False
    else:
        print('User not authenticated.', file=sys.stderr)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_user():
    form = AddUser()
    if form.validate_on_submit():
        # Extract values from form
        firstname = form.first_name.data
        lastname = form.last_name.data
        email = form.email.data
        address = form.address.data
        gender = form.gender.data
        major_id= form.major_id.data
        password= form.password.data
        
        # Create a  record to store in the DB
        u = User(user_id=username,first_name=firstname, last_name=lastname,email=email,address=address,gender=gender,password=password )

        # add record to table and commit changes
        db.session.add(u)
        db.session.commit()

        form.user.data = ''
        return redirect(url_for('add_user'))
    return redirect(url_for('index'))


@app.route('/block_access', methods=['GET', 'POST'])
@login_required
def access_record():
    # Verifying that user is an admin
    if is_admin():
        form = SelectUserForm()
        if form.validate_on_submit():
            # Extract Values from form
            user_toblock = form.user_id.data
           # search for user
            block =  db.session.query(User).filter_by(user_id = form.user.data).first()
            # create record to store in database
            
            # If record is found delete from DB table and commit changes
            if block is not None:
                db.session.add(b)
                db.session.commit()

            # Redirect to the view_all route (view function)
        return redirect(url_for('view')                       #Elvis REMINDER CHANGE TO HOMPAGE
    return render_template('selectuser.html', form=form)
    # Tell non-admin user they're not authorized to access route.
    else:
        return render_template('unauthorized.html')





@app.route('/view_profilepage')
def view():
    print(all, file=sys.stderr)
    return render_template('profilepage.html')


