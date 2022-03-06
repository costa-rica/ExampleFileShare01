from app_package import db, login_manager
from flask_login import UserMixin
from datetime import datetime, date
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous.serializer import Serializer
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
    

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    permission =db.Column(db.Text)
    time_stamp = db.Column(db.DateTime, default=datetime.now)
    file_tracker = db.relationship('FileTracker', backref='user', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        #TODO: Set expiration for serializer#########
        print(current_app.config['SECRET_KEY'])
        # s=Serializer(current_app.config['SECRET_KEY'], expires_sec)
        s=Serializer(current_app.config['SECRET_KEY'])
        # return s.dumps({'user_id': self.id}).decode('utf-8')
        print(s.dumps({'user_id': self.id}))
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Users.query.get(user_id)

    def __repr__(self):
        return f"Users('{self.id}','{self.email}','{self.permission}')"

class FileTracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.Text)
    time_stamp = db.Column(db.DateTime, default=datetime.now)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"FileTracker('{self.id}','{self.file_name}','{self.time_stamp}')"