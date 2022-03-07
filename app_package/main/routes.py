
from flask import Blueprint

from flask import render_template, url_for, redirect, flash, request, \
     current_app, send_from_directory
from app_package import db, bcrypt, mail
from app_package.models import Users
import sqlalchemy as sa
# from app_package.users.forms import LoginForm, RegistrationForm, \
#     ResetPasswordForm, AccessNewForm, AccessEditForm, RequestResetForm
from flask_login import login_required
import os
import shutil #copy file library
from app_package.main.utils import get_size_dict

main = Blueprint('main', __name__)


# @main.route("/upload_page", methods=["GET","POST"])
# @login_required
# def upload_page():

#     isExist = os.path.exists(current_app.config['UPLOAD_DIR'])
#     if not isExist:
#         os.makedirs(current_app.config['UPLOAD_DIR'])

#     upload_data_file_list = os.listdir(current_app.config['UPLOAD_DIR'])

#     size_list=[]
#     for i in upload_data_file_list:
#         size=os.path.getsize(os.path.join(current_app.config['UPLOAD_DIR'],i))
#         print('size::::', size)
#         if len(str(size))>9:
#             size= str(f"{round(size/10**9,1):,}") +' GB'
#         elif len(str(size))>3:
#             size= str(f"{round(size/10**6,2):,}") +' MB'
#         else:
#             size=str(f"{size:,}")+' bytes'
#         size_list.append(size)
    
#     files_info_lists=zip(upload_data_file_list,size_list)


#     if request.method == 'POST':

#         filesDict = request.files.to_dict()
#         formDict = request.form.to_dict()
        
#         # print('formDict:::',formDict)

#         # if request.files['media']:
#         if formDict.get('file_to_delete'):
#             os.remove(os.path.join(current_app.config['UPLOAD_DIR'],formDict.get('file_to_delete')))
#             return redirect(url_for('main.upload_page', files_info_lists=files_info_lists))
#         elif filesDict.get('upload_file'):
#             print('filesDict:::',filesDict)
#             uploadData=request.files['upload_file']
#             uploadData.save(os.path.join(current_app.config['UPLOAD_DIR'], uploadData.filename))
#             return redirect(url_for('main.upload_page', files_info_lists=files_info_lists))
#     return render_template('upload_page.html', files_info_lists=files_info_lists)

    
    
@main.route("/download_data_page", methods=["GET","POST"])
@login_required
def download_data_page():
    file_name=request.args.get('file_name')

    return send_from_directory(os.path.join(
        current_app.config['UPLOAD_DIR']),file_name, as_attachment=True)


@main.route("/upload", methods=["GET","POST"])
@login_required
def upload_page():

    #"Uploaded" files - server files like in the real thing
    isExist = os.path.exists(current_app.config['UPLOAD_DIR'])
    if not isExist:
        os.makedirs(current_app.config['UPLOAD_DIR'])

    upload_file_name_list = os.listdir(current_app.config['UPLOAD_DIR'])
    upload_file_dict=get_size_dict(upload_file_name_list)
    # uploaded_files_info_lists=zip(upload_data_file_list,size_list)

    #"Local" files - servers side files that are built to look like local client machine
    isExist = os.path.exists(current_app.config['TEST_DIR'])
    if not isExist:
        os.makedirs(current_app.config['TEST_DIR'])
        for i in range(0,2):
            with open(os.path.join(current_app.config['TEST_DIR'],f'test_0{i}.txt'), 'w') as newfile:
                newfile.write(f'Test file {i}')
                newfile.close


    local_dir_files=os.listdir(current_app.config['TEST_DIR'])
    # local_dir_files.remove('sub_directory')
    local_files_info_dict={i:[os.path.join(current_app.config['TEST_DIR'],i),False] for i in local_dir_files}
    print('local_dir_files::',local_dir_files)

    selected_files=''
    if request.args.get('selected_files'):
        request_items = request.args.to_dict(flat=False)
        selected_files = request_items.get('selected_files')
        for i in selected_files:
            local_files_info_dict[i] = [local_files_info_dict[i][0],True]


    if request.method == 'POST':
        formDict = request.form.to_dict()
        print('formDict:::', formDict)
        
        #select file for upload from "local" directory --In Modal
        if formDict.get('select_file')=='True':
            selected_files = [i[5:] for i,j in formDict.items() if i[:5]=='file_']
            return redirect(url_for('main.upload_page', selected_files=selected_files))
        
        #upload selected_files
        elif formDict.get('upload') == 'True':
            for i in selected_files:
                source= local_files_info_dict[i][0]
                destination=os.path.join(current_app.config['UPLOAD_DIR'],i)
                shutil.copyfile(source, destination)
            return redirect(url_for('main.upload_page'))

        #delete uploaded file
        elif formDict.get('file_to_delete'):
            os.remove(os.path.join(current_app.config['UPLOAD_DIR'],formDict.get('file_to_delete')))
            return redirect(url_for('main.upload_page', local_files_info_dict=local_files_info_dict))

    return render_template('upload_page_mock.html', selected_files=selected_files,
        local_files_info_dict=local_files_info_dict, upload_file_dict=upload_file_dict, len=len)