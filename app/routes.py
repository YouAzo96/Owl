from app import app
from flask import render_template, redirect, url_for
#from app.forms import 
from app import db
#from app.models import 
import sys

@app.route('/')
def hello():
    return render_template('index.html')

