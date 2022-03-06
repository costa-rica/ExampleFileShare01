from flask import current_app
# from flask_login import current_user
from app_package import db
from app_package.models import Users
import json

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

def remove_non_admin(logged_in_email):
    adminAccess=open(current_app.config['ADMIN_CREDENTIALS'],"r")
    data=json.loads(adminAccess.read())

    keep_emails = [i['email'] for i in data]
    keep_emails.append(logged_in_email)

    existing_emails = [i.email for i in Users.query.all()]
    for i in existing_emails:
        if i not in keep_emails:
            db.session.query(Users).filter(Users.email==i).delete()
            db.session.commit()