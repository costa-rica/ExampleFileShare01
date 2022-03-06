from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, \
    TextAreaField, DateTimeField, FloatField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app_package import db
from app_package.models import Users
from wtforms.widgets import PasswordInput

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()],id='password')
    submit = SubmitField('Complete')
    show_password = BooleanField('Show password')

    def validate_email(self, email):
        user=Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email already taken.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    # password = PasswordField('Password', validators=[DataRequired()],id='password')
    password = StringField('Password', widget=PasswordInput(hide_value=False), validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
    show_password = BooleanField('Show password')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')
    show_password = BooleanField('Show password')

class AccessNewForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    add_privilege = BooleanField('Give Add Privilege')
    submit = SubmitField('Add Permission')

class AccessEditForm(FlaskForm):
    add_privilege = BooleanField('Give Add Privilege')
    submit = SubmitField('Add Permission')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')