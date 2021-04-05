from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


# force loading of environment variables
load_dotenv('.flaskenv')

# Get the environment variables from .flaskenv
PASSWORD = os.environ.get('DATABASE_PASSWORD')
USERNAME = os.environ.get('DATABASE_USERNAME')
DB_NAME = os.environ.get('DATABASE_NAME')

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'owlpool'

# Add DB config
app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql+pymysql://'
                                        + USERNAME
                                        + ':'
                                        + PASSWORD
                                        + '@db4free.net/'
                                        + DB_NAME)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

<<<<<<< HEAD
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER=os.path.join(APP_ROOT, 'static', 'images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Create database connection and associate it with the Flask application
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view ='login'

from app import routes, models
from app.models import User, Announcement

db.create_all()

admin_check = User.query.filter_by(email='youssef@owl.edu').first()
if admin_check is None:
    admin = User(user_id=1,first_name='Youssef',last_name="Youssef",address='NULL', user_type='admin',major_id=1,email='youssef@owl.edu',gender='male',active=True)
    admin.set_password('password')
    db.session.add(admin)
    

db.session.commit()
