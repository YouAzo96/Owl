from app import app
from flask import render_template, redirect, url_for, flash,request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RegistrationForm,  LoginForm,BanForm,AddAnnouncement
from app import db
from sqlalchemy import update
from werkzeug.utils import secure_filename
from app.models import User, Major, User_Intrest, Rating, Intrest,Reports,Announcement
import sys
import os

@app.route('/', methods=['GET','POST'])
def index():
    all_ann = db.session.query(Announcement).order_by(Announcement.timestamp.desc()).all()
    form = AddAnnouncement()
    if current_user and not current_user.is_anonymous:
        user = current_user
    else: 
        user = ''
    if is_admin():
         if form.validate_on_submit():
             desc = form.description.data
             flag = form.flag.data
             ann = Announcement(admin_id='1',description= desc, flag = flag)
             db.session.add(ann)
             db.session.commit()
             form.description.data=''
             form.flag.data = ''
             return redirect(url_for('index'))
    return render_template('index.html',user=user, announcements = all_ann, form=form, isAdmin= is_admin())
    
 
def is_admin():

    if current_user.is_anonymous:
        return False;
        
    elif  current_user.user_type == "admin":
            return True;
    else: 
        return False;


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
        filename = False
        image = request.files['image']
        if form.password.data != form.password2.data:
            return render_template('register.html', title='SignUp', form=form, invalid_password=True)
        if image.filename != '':
            filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                 
        if  form.validate_email(email)== False:
            return render_template('register.html', title='SignUp', form=form, user_exists=True)
        
        # Create a  record to store in the DB
        if filename is not False:
            u = User(first_name=firstname, last_name=lastname,email=email,image=image.filename,address=address,gender=gender,major_id=major_id,active=True,user_type='user' )
            u.set_password(form.password.data)
            image.save(filename)
        else:
            u = User(first_name=firstname, last_name=lastname,email=email,image='',address=address,gender=gender,major_id=major_id,active=True,user_type='user' )
            u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()

        login_user(u)
        return redirect(url_for('index'))
    return render_template('register.html', title='SignUp', form=form)

@app.route('/profile', defaults={'user_id' : None})
@app.route('/profile/<user_id>')
def viewprofile(user_id):
    if user_id is None:
        user_profile=user =db.session.query(User).filter_by(user_id=current_user.user_id).first()
    else:
        user_profile = db.session.query(User).filter_by(user_id=user_id).first()
        if user_profile.active == False:
            return (redirect(url_for('index')))
        user = db.session.query(User).filter_by(user_id=current_user.user_id).first()
        
    if current_user.is_authenticated and user_id is None:
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
            overall = "."
        return render_template('profilepage.html',isAdmin = is_admin(),isMyProfile=featuresShow,user=user,user_profile=user_profile,rating=overall,major=major,interests=interestNames)
    else:
        return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin():
    if current_user is None:
        return render_template('login.html');   
    if   not current_user.is_authenticated:
        return render_template('login.html'); 
    if not is_admin():
        return render_template('login.html');     
    return render_template('admin.html',user=current_user)

@app.route('/reports')
@login_required
def reports():
    records = db.session.query(Reports).filter_by(status=1).all()
        
    return render_template('reports.html',isAdmin = is_admin(),user=current_user, reports=records)


@app.route('/banuser/<reported_id>', methods=['GET','POST'])
@login_required
def ban(reported_id):
    if reported_id is not None: 
        stmt =update(User).values(active=(False)).where(User.user_id == reported_id)
        stmt1= Reports.__table__.delete().where(Reports.reported_id==reported_id)
        db.session.execute(stmt)
        db.session.execute(stmt1)
        db.session.commit()
        return redirect(url_for('reports'))
    return redirect(url_for('banwithid'))      


@app.route('/banuser',methods=['GET','POST'])
@login_required
def banwithid():
        form = BanForm()
        if form.validate_on_submit():
            user_to_ban = db.session.query(User).filter_by(user_id = form.user_id.data).first()
            if user_to_ban:
                stmt =update(User).values(active=(False)).where(User.user_id == form.user_id.data)
                db.session.execute(stmt)
                db.session.commit()
                form.user_id.data=''
                return redirect(url_for('banwithid'))
            else:
                return render_template('ban.html',isAdmin = is_admin(),user=current_user,form = form, notFound=True)
        return render_template('ban.html',isAdmin = is_admin(),user=current_user, form = form)

