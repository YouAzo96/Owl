from app import app
from flask import render_template, redirect, url_for

from app.forms import BanForm,AddAnnouncement
from app.models import User, Reports,Announcement
from app import db
from sqlalchemy import update
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

@app.route('/admin')
@login_required
def admin():
    if current_user is None:
        return render_template('login.html');   
    if   not current_user.is_authenticated:
        return render_template('login.html'); 
    if not is_admin():
        return render_template('login.html');     
    return render_template('admin.html', name=current_user.first_name)

@app.route('/reports')
def reports():
    records = db.session.query(Reports).filter_by(status=1).all()
        
    return render_template('reports.html', reports=records)


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


@app.route('/banuser')
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
                return redirect(url_for('ban'))
            else:
                return render_template('ban.html',form = form, notFound=True)
        return render_template('ban.html', form = form)

