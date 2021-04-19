from app import app
<<<<<<< Updated upstream
from flask import render_template, redirect, url_for
from app.forms import AddAnnouncement
from app.models import Announcement
from flask_login import current_user, login_required
=======
from flask import render_template, redirect, url_for, flash,request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app.forms import RegistrationForm,  LoginForm,BanForm,AddAnnouncement, SchedulerForm
from app import db
from sqlalchemy import update, func
from werkzeug.utils import secure_filename
from app.models import User, Major, User_Intrest, Rating, Intrest,Reports,Announcement, Requests, Ride, Ride_Passengers
>>>>>>> Stashed changes
import sys

@app.route('/', methods=['GET','POST'])
def index():
    all_ann = db.session.query(Announcement).all()
    form = AddAnnouncement()
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
    return render_template('index.html', announcements = all_ann, form=form, isAdmin= is_admin())
    
 
def is_admin():
    if current_user & current_user.role == "admin":
        return True;
    else: 
        return False;

<<<<<<< Updated upstream
=======

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
        driver_history = db.session.query(Ride).filter_by(driver_id=user.user_id). \
            filter_by(completed = True).all()
        passenger_history = db.session.query(Ride, Ride_Passengers).filter_by(completed = True). \
            join(Ride_Passengers).filter_by(passenger_id=user.user_id).all()

        driver_active = db.session.query(Ride).filter_by(driver_id=user.user_id). \
                            filter_by(completed = False).all()
        passenger_active = db.session.query(Ride, Ride_Passengers).filter_by(completed = False). \
                               join(Ride_Passengers).filter_by(passenger_id=user.user_id).all()

        #need to know the number of rows of passengers for a given ride
        request_join = db.session.query(User,Ride,Requests).select_from(User).join(Ride).join(Requests). \
            filter(Ride.driver_id == current_user.user_id).all()
        request_sent = db.session.query(User,Ride,Requests).select_from(User).join(Ride).join(Requests). \
            filter(Requests.requester == current_user.user_id).all()

        # query may not be correct
        
        total=0
        for rating in ratings:
            total += rating.stars
        if total >0:
            overall = total /len(ratings)
        else:
            overall = "."
        return render_template('profilepage.html',isAdmin = is_admin(),isMyProfile=featuresShow,user=user,user_profile=user_profile,rating=overall,major=major,interests=interestNames, \
            driver_history=driver_history, passenger_history=passenger_history, driver_active=driver_active, passenger_active=passenger_active, \
               request_join=request_join, request_sent=request_sent)
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
        return redirect(url_for('index'));  
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

@app.route('/rides')
def ridebrowser():
    # we need rides list called : rides 
    # we need number of reuests each ride has: num_of_requests
    # we need first and last name and image of each the driver as a list: drivers
    if not current_user.is_anonymous:
        user = current_user
    else:
        user = ''
    num_of_passengers = db.session.query(Ride_Passengers.ride_id, func.count(Ride_Passengers.ride_id).label('count')).group_by(Ride_Passengers.ride_id).all()
 
    rides = db.session.query(Ride).order_by(Ride.start_date.desc()).all()
    drivers_ids =[]
    for ride in rides:
        drivers_ids.append(ride.driver_id)

    drivers = db.session.query(User.user_id,User.first_name, User.last_name, User.image).filter(User.user_id.in_(drivers_ids)).all()
    print(drivers, file=sys.stderr)
    return render_template('rides.html',user=user,drivers = drivers, rides = rides, num_of_passengers = num_of_passengers)


@app.route('/join/<ride_id>', methods=['GET','POST'])
@login_required
def joinride(ride_id):
    if ride_id is None or ride_id=='':
        return redirect(url_for('index'))
    elif current_user.is_anonymous:
        return redirect(url_for('login'))
        
    request = Request(ride_id = ride_id, requester=current_user)
    db.session.add(request)
    db.session.commit()
    
    return redirect(url_for('profilepage.html#myrequests'))

@app.route('/cancel_driver/<ride_id>', methods=['GET', 'POST'])
@login_required
def cancelride(ride_id): # may need another field in ride called "canceled"
    if ride_id is None or ride_id=='':
        return redirect(url_for('index'))
    elif current_user.is_anonymous:
        return redirect(url_for('login'))
        
    selected_ride = db.session.query(Ride).filter_by(ride_id=ride_id). \
        filter_by(driver_id=current_user.user_id).first() #checks if being called by driver of ride
    
    if selected_ride:
        
        db.session.delete(selected_ride)
        db.session.commit()

        del_pas = db.session.query(Ride_Passengers).filter_by(ride_id=ride_id).all()
        db.session.delete(del_pas)
        db.session.commit() # deletes all records of passengers for ride.
        

    else:
        return redirect(url_for('viewprofile')) # user cant del record if not driver
    return redirect('profilepage.html#Rides')

@app.route('/cancel_passenger/<ride_id>')
@login_required
def cancelride2(ride_id):
    if ride_id is None or ride_id=='':
        return redirect(url_for('index'))
    elif current_user.is_anonymous:
        return redirect(url_for('login'))
        
    selected_ride = db.session.query(Ride_Passengers).filter_by(ride_id=ride_id). \
        filter_by(passenger_id=current_user.user_id).first()

    if selected_ride:
    
        db.session.delete(selected_ride)
        db.session.commit()

    else:
        return redirect(url_for('viewprofile')) # user cant del record if not a passenger
    return redirect('profilepage.html#Rides')
    








>>>>>>> Stashed changes
