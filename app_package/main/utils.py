import os
from flask import current_app
def get_size_dict(upload_file_name_list):
    upload_file_dict={}
    for i in upload_file_name_list:
        size=os.path.getsize(os.path.join(current_app.config['UPLOAD_DIR'],i))
        
        if len(str(size))>9:
            size= str(f"{round(size/10**9,1):,}") +' GB'
        elif len(str(size))>3:
            size= str(f"{round(size/10**6,2):,}") +' MB'
        else:
            size=str(f"{size:,}")+' bytes'
        upload_file_dict[i]=size
    return upload_file_dict