from app import db 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlalchemy

class User (UserMixin, db.Model):
    __tablename__='user'
    user_id = db.Column(db.Integer , primary_key=True)
    first_name =db.Column (db.String (100))
    last_name = db.Column (db.String (100))
    user_type = db.Column (db.String (5),default="user")
    email = db.Column (db.String(100), unique=True)
    major_id = db.Column (db.Integer, sqlalchemy.ForeignKey('major.major_id'))
    address = db.Column (db.String (150),nullable=True)
    gender = db.Column (db.String (10))
    image= db.Column(db.String(50),nullable=True)
    active = db.Column (db.Boolean, default='1')
    password_hash = db.Column(db.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password (self, password):
        return check_password_hash(self,password_hash,password)
   # @login.user_loader
    def loader_user(user_id):
         return db.session.query(User).get(int(user_id))


class Ride(db.Model):
    __tablename__='ride'
    ride_id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer,sqlalchemy.ForeignKey('user.user_id'), nullable=False)
    passenger_id = db.Column(db.Integer,sqlalchemy.ForeignKey('user.user_id'), nullable=False)
    destination = db.Column(db.String (100), unique=True)

class Announcement(db.Model):
    __tablename__='announcement'
    announcement_id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column (db.Integer, sqlalchemy.ForeignKey('user.user_id'))
    description = db.Column (db.String (100))
    flag = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime,nullable=False,default=datetime.now())

class Rating(db.Model):
    __tablename__='rating'
    rating_id = db.Column(db.Integer, primary_key=True)
    writer_id = db.Column (db.Integer, sqlalchemy.ForeignKey('user.user_id'),nullable=False)
    reciver_id = db.Column (db.Integer, sqlalchemy.ForeignKey('user.user_id'),nullable=False)
    description = db.Column(db.String (100))
    stars = db.Column(db.Integer)

class Member(db.Model):
    __tablename__='member'
    group_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)

class Major (db.Model):

    __tablename__='major'
    major_id = db.Column(db.Integer, primary_key=True)
    major_name = db.Column(db.String (100), unique=True)

class User_Intrest(db.Model):
    __tablename__='user_intrest'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer ,sqlalchemy.ForeignKey('user.user_id'))
    intrest_id = db.Column(db.Integer, sqlalchemy.ForeignKey('intrest.intrest_id'))

class Intrest (db.Model):
    __tablename__='intrest'
    intrest_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

class IntrestGroup(db.Model):
    __tablename__='intrestgroup'
    group_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), unique=True)
    group_name = db.Column(db.String(100), unique=True)

class Post(db.Model):
    __tablename__='post'
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column (db.Integer, sqlalchemy.ForeignKey ('user.user_id'), nullable=False)
    group_id = db.Column(db.Integer, sqlalchemy.ForeignKey ('intrestgroup.group_id'), nullable=False)
    content = db.Column(db.String(100), unique=True)
    timestamp = db.Column(db.DateTime,nullable=False,default=datetime.now())

class Reports (db.Model):
    __tablename__='reports'
    report_id = db.Column(db.Integer, primary_key=True)
    reported_id = db.Column(db.Integer ,sqlalchemy.ForeignKey('user.user_id'))
    reporter_id = db.Column(db.Integer ,sqlalchemy.ForeignKey('user.user_id'))
    description = db.Column(db.String(100))
    status = db.Column(db.Integer)
    #the status column is a switch that hold zero or one. when zero meaans the report has not resolved yet.
