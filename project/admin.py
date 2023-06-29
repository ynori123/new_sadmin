from flask import Blueprint,request,render_template,redirect,url_for
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
        data.append([q.name, q.wages, q.email])
    
    return render_template(
        'employee.html',
        data=data
    )

@admin.route('/admin/employee/<name>', methods=['GET','POST'])
def employee_update(name :str):
    if request.method == 'GET':
        query = db.session.query(User).filter_by(name=name).first()
        data = [query.name, query.wages, query.email]
        return render_template(
            'employee_update.html',
            data=data
        )
    
    elif request.method == 'POST':
        user = db.session.query(User).filter_by(name=name).first()
        if request.form.get('email') == '':
            user.delete()
            db.session.commit()
            mes = "ユーザ{}の削除が完了しました。"
        else:
            user.name = request.form.get('name')
            user.wages = request.form.get('wages')
            user.email = request.form.get('email')
            db.session.commit()
            mes = "ユーザの情報の変更が完了しました。"
        return redirect(url_for('admin.employee'))
