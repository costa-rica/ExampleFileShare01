from flask import Flask
from app_package.config import ConfigDev, ConfigProd
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from flask_mail import Mail


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.upload'
login_manager.login_message_category = 'success'
mail = Mail()

if os.environ.get('COMPUTERNAME')=='CAPTAIN2020':
    config_class=ConfigDev
else:
    config_class=ConfigProd

def create_app(config_class=config_class):
    
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app_package.users.routes import users
    from app_package.main.routes import main
    from app_package.error_handlers.routes import error
    
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(error)
    
    return app