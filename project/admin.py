from flask import Blueprint,request,flash,render_template,redirect,url_for
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

@admin.route('/admin/edit', methods=['GET'])
def edit():
    mon = []
    tue = []
    wed = []
    thu = []
    fri = []
    sat = []
    sun = []
    week_list = list('月火水木金土日')

    for i in range(7):
        query = db.session.query(PostedShift).filter_by(dayofweek=i).all()
        # 提出されたシフトデータベースを曜日ごとに振り分け
        for q in query:
            if i == 0:
                mon.append([q.name,q.begin])
            elif i == 1:
                tue.append([q.name,q.begin])
            elif i == 2:
                wed.append([q.name,q.begin])
            elif i == 3:
                thu.append([q.name,q.begin])
            elif i == 4:
                fri.append([q.name,q.begin])
            elif i == 5:
                sat.append([q.name,q.begin])
            elif i == 6:
                sun.append([q.name,q.begin])

    # return data
    return render_template(
        'edit.html',
        week_list=week_list,
        data = [
            mon,tue,wed,thu,fri,sat,sun
        ]
        
    )

@admin.route('/admin/edit', methods=['POST'])
def update_edit():
    

    return "シフトを公開しました。"


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
        try:
            query = db.session.query(User).filter_by(name=name).first()
            data = [query.name, query.wages, query.email]
            return render_template(
                'employee_update.html',
                data=data
            )
        except:
            return "例外が発生しました。"
    elif request.method == 'POST':
        user = db.session.query(User).filter_by(name=name).first()
        if request.form.get('email') == '':
            user.delete()
            db.session.commit()
            mes = "ユーザ{}の削除が完了しました。"
            # flash message
            flash(mes)
        else:
            user.name = request.form.get('name')
            user.wages = request.form.get('wages')
            user.email = request.form.get('email')
            db.session.commit()
            mes = "ユーザの情報の変更が完了しました。"
            # flash message
            flash(mes)
        return redirect(url_for('admin.employee'))
