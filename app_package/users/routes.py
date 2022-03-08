from flask import Blueprint
from flask import render_template, url_for, redirect, flash, request, \
     current_app, send_from_directory, abort
from app_package import db, bcrypt, mail
from app_package.models import Users
import sqlalchemy as sa
from app_package.users.forms import LoginForm, RegistrationForm, \
    ResetPasswordForm, AccessNewForm, AccessEditForm, RequestResetForm
from flask_login import login_user, current_user, logout_user, login_required
import os
from flask_mail import Message
import json
from app_package.users.utils import build_db, remove_non_admin, \
    add_admin_users

users = Blueprint('users', __name__)


@users.route("/", methods=["GET","POST"])
@users.route("/home", methods=["GET","POST"])
def home():

    #Handle access and database
    if current_user.is_authenticated:
        print('HOME SCReen::', current_user.email)
        return redirect(url_for('main.upload_page'))
    elif 'users' in sa.inspect(db.engine).get_table_names():
        print('db already exists')
    else:
        build_db()#and add admin users
        

    form = LoginForm()

    if request.args.get('email_entry'):
        form.email.data=request.args.get('email_entry')
        form.password.data=request.args.get('pass_entry')

    if form.validate_on_submit():
        #remove anyone not current user or in admin.json
        remove_non_admin()
        print('All Users:::', Users.query.all())

        # if not in db, add admin.json user missing
        add_admin_users()
        
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.upload_page'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('home.html', form=form)

@users.route("/register", methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.upload_page'))
    form = RegistrationForm()
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(email=form.email.data, password=hashed_password, permission='1')
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('users.home'))
    return render_template('register.html', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.home'))


@users.route("/password_change", methods=["GET","POST"])
@login_required
def password_change():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        formDict = request.form.to_dict()
        if formDict.get('no_change') != 'guest_email':
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated!', 'success')
        else:
            flash('This user cannot change passwords.', 'warning')
    return render_template('password.html', form=form)



def send_new_user_email(user):
    # token = user.get_reset_token()
    msg = Message('Access DD File Share',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    msg.body = f'''Visit the following link:
{url_for('users.home', _external=True)}

Login with your email address and the current password is your email address before the @
'''
    mail.send(msg)



@users.route("/access", methods=["GET","POST"])
@login_required
def access():

    all_users=[(i.id,i.email,i.permission) for i in Users.query.all()]

    form=AccessNewForm()

    if form.submit.data and form.validate_on_submit():
        # formDict = request.args.to_dict()
        formDict = request.form.to_dict()
        new_email=form.email.data
        hashed_password = bcrypt.generate_password_hash(new_email[:new_email.find('@')]).decode('utf-8')
        
        user=Users(email=new_email, password=hashed_password, permission=form.add_privilege.data)
        db.session.add(user)
        db.session.commit()
        
        #TODO: Send email to new user with password
        if form.send_email.data:
            send_new_user_email(user)
            flash(f'{new_email} has been granted access!', 'success')
        else:
            flash(f'{new_email} has access!', 'success')
        return redirect(url_for('main.upload_page'))

    return render_template('access.html', form=form, all_users=all_users, len=len)



@users.route("/edit_access", methods=["GET","POST"])
@login_required
def access_edit():
    all_users=[(i.id,i.email,i.permission) for i in Users.query.all()]
    print('all_users::',all_users)
    if current_user.email =='guest@DashAndData.com':
        all_users.remove((1,'guest@DashAndData.com','1'))
    else:
        all_users.remove((1,'guest@DashAndData.com','1'))
        for i in all_users:
            if i[1]==current_user.email:
                all_users.remove(i)


    if request.method == 'POST':
        formDict = request.form.to_dict()
        if formDict.get('update_button') == 'True':

            for i in all_users:

                if i[2] == '1' and not formDict.get(f'add_privilege_for {i[0]}'):

                    Users.query.get(i[0]).permission = 0
                    db.session.commit()
                    flash(f'{i[1]} has had privileges removed', 'warning')
                if i[2] == '0' and formDict.get(f'add_privilege_for {i[0]}'):
                    Users.query.get(i[0]).permission = 1
                    db.session.commit()
                    flash(f'{i[1]} has been granted add privileges!', 'success')
        elif formDict.get('delete_button')=='':
            db.session.query(Users).filter(Users.email==formDict.get('delete_record_email')).delete()
            db.session.commit()
        return redirect(url_for('users.access_edit'))
    return render_template('access_edit.html', all_users=all_users, len=len)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.upload_page'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password (check main and spam folders).', 'success')
        return redirect(url_for('users.home'))
    return render_template('reset_request.html', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.upload_page'))
    user = Users.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.home'))
    return render_template('password.html', title='Reset Password', form=form)