from app import app
from flask import render_template, redirect, url_for, flash,request,session
from flask_login import login_user, logout_user, login_required, current_user,LoginManager
from app.forms import RegistrationForm,  LoginForm,BanForm,AddAnnouncement, SchedulerForm,ChangePasswordForm,EditProfileForm,FilterForm
from app.email import send_email
from app.token import generate_confirmation_token, confirm_token
from app import db
from sqlalchemy import update, func
from werkzeug.utils import secure_filename
from werkzeug import *
from app.models import User, Major, User_Intrest, Rating, Intrest,Reports,Announcement, Requests, Ride, Ride_Passengers
import sys 
import os
from sqlalchemy_filters import apply_filters
import pdb, pprint

@app.route('/', methods=['GET','POST'])
def index():
    if session.get('alert'):
        alert = session['alert']
        session.pop('alert',None)
    else:
        alert = None
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
             session['alert']= 'Announcement Added!'
             return redirect(url_for('index'))
    return render_template('index.html',user=user, announcements = all_ann, form=form, isAdmin= is_admin(),alert=alert)
    
 
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
    if current_user.is_authenticated and current_user.confirmed:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # Query DB for user by username
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user is None:
            return render_template('login.html', form=form, user_not_found=True) 
        if user.active:
            if user.check_password(form.password.data):
                if user.confirmed:
                    login_user(user)
                    session['alert']= 'Welcome '+user.first_name
                    if  request.args:
                        if request.args['next']:
                            next_url = request.args['next']
                            return redirect(next_url)
                    return redirect(url_for('index'))
                else:
                    login_user(user)
                    return render_template('unconfirmed.html', user=user)
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
        if form.clean_email() == False:
            return render_template('register.html', title='SignUp', form=form, email_format=True)
        else:
            email = form.clean_email()
        address = form.address.data
        gender = form.gender.data
        major_id= form.major_id.data
        filename = False
        confirmed=False
        image = request.files['image']
        if form.password.data != form.password2.data:
            return render_template('register.html', title='SignUp', form=form, invalid_password=True)
        if image.filename != '':
            filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                 
        if  form.validate_email(email)== False:
            return render_template('register.html', title='SignUp', form=form, user_exists=True)
        
        # Create a  record to store in the DB
        if filename is not False:
            u = User(first_name=firstname, last_name=lastname,email=email,image=image.filename,address=address,gender=gender,major_id=major_id,active=True,user_type='user' ,confirmed=confirmed)
            u.set_password(form.password.data)
            image.save(filename)
        else:
            u = User(first_name=firstname, last_name=lastname,email=email,image='',address=address,gender=gender,major_id=major_id,active=True,user_type='user',confirmed=False )

            u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        SendToken(u.email)
        return redirect(url_for('login'))
    return render_template('register.html', title='SignUp', form=form)


@app.route('/dn/<ann_id>')
@login_required
def delete_announcement(ann_id):
    if not is_admin():
        return redirect(url_for('index'))
    ann=Announcement.query.filter_by(announcement_id=ann_id).first()
    db.session.delete(ann)
    db.session.commit()
    session['alert']='Announcement Deleted!'
    return redirect(url_for('index'))
        
@app.route('/Send_Token/<email>')
@login_required
def send_token(email):
    if email is not None:
        SendToken(email)
        return render_template('unconfirmed.html', user=current_user)
    else:
        return redirect(url_for('index'))
    
def Notifications(email,message):
    try:
        html=render_template('Notifications.html',message=message )
        subject= "OWLPOOL NOTIFICATION"
        send_email(email, subject, html)
        session['alert']= "Email Sent"
    except:
        session['alert']= "Email not Sent"
        return False
    return True

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
        
@app.route('/confirm')
@app.route('/confirm/<token>')
@login_required
def confirm_email(token):
    if token is None:
        return redirect(url_for('logout'))
    try:
        email = confirm_token(token)
    except:
        return redirect(url_for('logout'))
    
    user = db.session.query(User).filter_by(email = email).first()
    user.confirmed = True
    db.session.add(user)
    db.session.commit()
    Notifications(user.email,"Thank You For Signing up to OWLPOOL. We Wish You have a safe Journey.")
    return redirect(url_for('index'))

@app.route('/profile', defaults={'user_id' : None})
@app.route('/profile/<user_id>')
def viewprofile(user_id):
    if user_id is None and current_user.is_anonymous:
        return redirect(url_for('index'))
        
    if user_id is None:
        user_profile=user =db.session.query(User).filter_by(user_id=current_user.user_id).first()

    elif user_id is not None and current_user.is_anonymous:
        user_profile =db.session.query(User).filter_by(user_id=user_id).first()
        if user_profile.active == False:
             return (redirect(url_for('index')))
        user = None
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
        return redirect(url_for('login'));  
    if   not current_user.is_authenticated:
        return redirect(url_for('login'));  
    if not is_admin():
        return render_template('login.html');     
    return render_template('admin.html',user=current_user)



@app.route('/scheduler', methods=['GET','POST'])
@login_required 
def scheduler():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
        
    form = SchedulerForm()
    time_error =  date_error = False
    if  form.validate_on_submit():
        from_location = form.from_location.data
        to_location = form.to_location.data
        start_time = form.start_time.data.strftime('%H:%M:%S')
        end_time = form.end_time.data.strftime('%H:%M:%S')
        start_date = form.start_date.data
        end_date = form.end_date.data
        max_passengers = form.max_passengers.data
        if start_date == end_date :
            if start_time >  end_time :
                 time_error = True
        if start_date > end_date :
           date_error = True

        if time_error or date_error:
             return render_template ('scheduler.html' ,form=form, time_error=time_error, date_error=date_error)
        ride = Ride(driver_id=current_user.user_id,from_location=from_location,to_location=to_location,start_time=start_time,end_time=end_time, start_date=start_date, end_date=end_date, max_passengers=max_passengers)
        db.session.add(ride)
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template ('scheduler.html' ,form=form, time_error=time_error, date_error=date_error)

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

@app.route('/rides', methods=["GET","POST"])
@login_required
def ridebrowser():
    if not current_user.is_anonymous:
        user = current_user
    else:
        redirect(url_for('login'))
    # we need rides list called : rides 
    # we need number of reuests each ride has: num_of_requests
    # we need first and last name and image of each the driver as a list: drivers
    form = FilterForm()
    filled=[]
    if request.method=="POST":
        for val in request.form :
            if request.form.get(val) !='':
                filled.append(val)
    rides = db.session.query(Ride).filter(Ride.driver_id != user.user_id).\
                                filter(Ride.completed==False).order_by(Ride.start_date.desc())   
    filter_spec=[]
    if filled:
        del filled[0]
        del filled[len(filled)-1]
        for att in filled:
            filter_spec.append({'field':att,'op':'==','value':request.form.get(att)})    
        rides = apply_filters(rides,filter_spec).all()
    else: 
        rides = rides.all()
    num_of_passengers = db.session.query(Ride_Passengers.ride_id, func.count(Ride_Passengers.ride_id).label('count')).group_by(Ride_Passengers.ride_id).all()
    drivers_ids =[]
    for ride in rides:
        drivers_ids.append(ride.driver_id)
    drivers = db.session.query(User.user_id,User.first_name, User.last_name, User.image).filter(User.user_id.in_(drivers_ids)).all()
    return render_template('rides.html',form=form,user=user,drivers = drivers, rides = rides, num_of_passengers = num_of_passengers)


@app.route('/join/<ride_id>', methods=['GET','POST'])
@login_required
def joinride(ride_id):
    if ride_id is None or ride_id=='':
        return redirect(url_for('index'))
    elif current_user.is_anonymous:
        return redirect(url_for('login'))
        
    request = Requests(ride_id=ride_id, requester=current_user.user_id)
    db.session.add(request)
    db.session.commit()
    return redirect(url_for('viewprofile'))

@app.route('/edit_profile',methods=['GET', 'POST'])
@login_required
def editprofile():
    user = current_user
    form=EditProfileForm(major_id=user.major_id)
    if form.validate_on_submit():
        address = form.address.data
        major_id= form.major_id.data
        filename = False
        image = request.files['image']
        if image.filename != '':
            filename= os.path.join(app.config['UPLOAD_FOLDER'],image.filename)
        if filename is not False: 
            user.image = image.filename
            image.save(filename)
        user.major_id = major_id 
        user.address = address
        db.session.commit()
        session['alert']="Profile Updated!"
        return redirect(url_for('viewprofile'))
    return render_template('editprofile.html', form=form, user=user,user_profile=user)


@app.route('/change_password',methods=['GET', 'POST'])
@login_required
def change_password():
    user=current_user
    form= ChangePasswordForm()
    if form.validate_on_submit():
        old_password = form.current_password.data
        new_password = form.password.data
        confirm_password = form.password2.data
        if user.check_password(old_password):
            if new_password == confirm_password:
                user.set_password(new_password)
                db.session.commit()
                session['alert']="Password Changed!"
                return redirect(url_for('index'))
            else:
               return render_template('changepassword.html', form=form, pass_not_match=True, user=user) 
        else:
            return render_template('changepassword.html', form=form, invalid_pass=True, user=user) 

    return render_template('changepassword.html', form=form, user=user) 


def SendToken(email):
    try:
        token = generate_confirmation_token(email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('confirmationtest.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(email, subject, html)
        session['alert']= "Confirmation Email Sent. Check your email."
        return True
    except:
        session['alert']= "Confirmation Email NOT Sent. Check with your administrator."
        return False
