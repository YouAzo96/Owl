from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RegistrationForm,  LoginForm
from app import db
from app.models import User, Major, User_Intrest, Rating, Intrest
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




@app.route('/sign_up', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
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

@app.route('/profile', defaults={'user_id' : None})
@app.route('/profile/<user_id>')
def viewprofile(user_id):
    if user_id is None:
        user_id = current_user.user_id
    user =db.session.query(User).filter_by(user_id=user_id).first()
    if current_user.is_authenticated:
        if current_user.user_id == user_id:
            featuresShow = True
        else:
            featuresShow = False
    if user is not None:
        tmp_interests_ids = db.session.query(User_Intrest.intrest_id).filter_by(user_id=user_id).all()
        interests_ids = []
        for intr in tmp_interests_ids:
                    interests_ids.append(intr.intrest_id)

        interestNames = db.session.query(Intrest.name).filter(Intrest.intrest_id.in_(interests_ids)).all()
        major = db.session.query(Major).filter_by(major_id=user.major_id).first() 
        ratings = db.session.query(Rating).filter_by(reciver_id = user.user_id).all()
        total=0
        for rating in ratings:
            total += rating.stars
        if total >0:
            overall = total /len(ratings)
        else:
            overall = "N/A"
        return render_template('profilepage.html',isMyProfile=featuresShow,user=user,rating=overall,major=major,interests=interestNames)
    else:
        return redirect(url_for('index'))

