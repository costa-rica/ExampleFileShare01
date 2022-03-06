from flask import current_app
# from flask_login import current_user
from app_package import db
from app_package.models import Users
import json
import datetime

def build_db():
    db.create_all()
    # print('db created')

    #add admin users
    f=open(current_app.config['ADMIN_CREDENTIALS'],"r")
    data=json.loads(f.read())
    for i in data:
        db.session.add(Users(email=i['email'],password=i['password'],permission=i['permission']))
        db.session.commit()
    # print('admin users added!')

def remove_non_admin():
    #3 emails that stay in database all the time
    adminAccess=open(current_app.config['ADMIN_CREDENTIALS'],"r")
    data=json.loads(adminAccess.read())
    keep_emails = [i['email'] for i in data]

    #Get all registerd users
    all_users=Users.query.all()
    all_users=[i.email for i in all_users]

    #remove all registered users not part of admin (3) that are older than 1 day
    new_users = list(set(all_users)-set(keep_emails))
    for i in new_users:
        difference = datetime.datetime.now() - db.session.query(Users).filter(Users.email==i).first().time_stamp
        if difference.days>1:
            db.session.query(Users).filter(Users.email==i).delete()
            db.session.commit()

def add_admin_users():
    f=open(current_app.config['ADMIN_CREDENTIALS_2'],"r")
    admin_cred_dict=json.loads(f.read())

    all_users=Users.query.all()
    all_users=[i.email for i in all_users]

    for i in admin_cred_dict.keys():
        if i not in all_users:
            db.session.add(Users(email=i,password=admin_cred_dict[i]['password'],permission=admin_cred_dict[i]['permission']))
            db.session.commit()