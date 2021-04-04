from app import app
from flask import render_template, redirect, url_for
from app import db
from app.forms import AddAnnouncement
from app.models import Announcement
from flask_login import current_user, login_required
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

