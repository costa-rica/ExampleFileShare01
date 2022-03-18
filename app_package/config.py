import os
import json

if os.environ.get('COMPUTERNAME')=='CAPTAIN2020':
    with open(r"C:\Users\captian2020\Documents\config_files\config_ddFileShare01.json") as config_file:
        config = json.load(config_file)
else:
    with open('/home/ubuntu/applications/config_ddFileShare01.json') as config_file:
        config = json.load(config_file)

class ConfigDev:
    DEBUG = True
    SECRET_KEY = config.get('SECRET_KEY_UPLOADER')
    SQLALCHEMY_DATABASE_URI = config.get('SQL_URI_DDFILESHARE01')
    MAIL_SERVER = config.get('MAIL_SERVER_MSOFFICE')
    MAIL_PORT = config.get('MAIL_PORT')
    MAIL_USE_TLS = True
    MAIL_PASSWORD = config.get('MAIL_PASSWORD_DD')
    MAIL_USERNAME = config.get('MAIL_EMAIL_DD')

    UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'static','upload')
    TEST_DIR = os.path.join(os.path.dirname(__file__), 'static','test_files')
    ADMIN_CREDENTIALS =config.get('ADMIN_CREDENTIALS')
    ADMIN_CREDENTIALS_2 =config.get('ADMIN_CREDENTIALS_2')

class ConfigProd:
    DEBUG = False
    SECRET_KEY = config.get('SECRET_KEY_UPLOADER')
    SQLALCHEMY_DATABASE_URI = config.get('SQL_URI_DDFILESHARE01')
    MAIL_SERVER = config.get('MAIL_SERVER_MSOFFICE')
    MAIL_PORT = config.get('MAIL_PORT')
    MAIL_USE_TLS = True
    MAIL_PASSWORD = config.get('MAIL_PASSWORD_DD')
    MAIL_USERNAME = config.get('MAIL_EMAIL_DD')

    UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'static','upload')
    TEST_DIR = os.path.join(os.path.dirname(__file__), 'static','test_files')
    ADMIN_CREDENTIALS =config.get('ADMIN_CREDENTIALS')
    ADMIN_CREDENTIALS_2 =config.get('ADMIN_CREDENTIALS_2')
    
