from flask import Blueprint,request,render_template
from flask_sqlalchemy import SQLAlchemy
from . import db

admin = Blueprint('admin', __name__,template_folder='templates/admin_templates')

@admin.route('/admin/')
def index():
    return render_template(
        'ad_index.html'
    )

@admin.route('/admin/message',methods=['GET','POST'])
def message():
    if request.method == 'GET':
        return render_template(
            'admin_templates/send_message.html'
        )
    elif request.method == 'POST':
        sender = request.form.get('sender')
        mes = request.form.get('mes')
        return(
            "a"
        )

from .models import PostedShift,FinalShift,User

@admin.route('/admin/edit')
def edit():
    return "edit"
@admin.route('/admin/employee')
def employee():
    query = db.session.query(User).all()
    data = []
    for q in query:
        data.append([q.name, q.email, q.wages])
    
    return render_template(
        'employee.html',
        data=data
    )


