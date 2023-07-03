from flask import Blueprint,render_template, request,jsonify,send_from_directory, url_for
from flask_login import login_required,current_user
from . import db
import queue

main = Blueprint('main', __name__)

message = ()

import os
@main.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(main.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )

import datetime
@main.route('/')
def index():
    dt :datetime = datetime.datetime.now()
    message = [dt.date(), 'hello', "Admin"]
    return render_template(
        'index.html',
        recent = "a",
        today = dt.date(),
        log = message
    )
from .models import User
@main.route('/profile')
@login_required
def profile():
    query = db.session.query(User).filter_by(name=current_user.name).first()
    wages = query.wages
    if wages == None or wages == "":
        wages="不明"
    return render_template(
        'profile.html',
        name=current_user.name,
        wages = wages,
    )

from .models import PostedShift,FinalShift
from .shift import escape
@main.route('/shiftform', methods=['GET', 'POST'])
@login_required
def shiftform():
    if request.method == 'POST':
        user = request.form.get('username')
        # 初めての送信からどうかを確かめる
        try:
            # 初めてであれはここでエラー
            query = db.session.query(FinalShift).filter_by(name=user).all()
            for item in query:
                item.begin = escape(request.form.get('form'+str(i)))
            db.session.commit()
            pass
        except:
            for i in range(7):
                db.session.add(
                    PostedShift(
                        dayofweek = i,
                        name = user,
                        begin = escape(request.form.get('form'+str(i)))
                    )
                )
                db.session.commit()

        return request.form

    elif request.method == 'GET':
        user = current_user.name
        data :list[str] = []
        try:
            # すでに入力したデータを取り出す
            query = db.session.query(FinalShift).filter_by(name=user).all()
            for item in query:
                data.append(item.begin)

        except:
            # エラーが発生したら空配列を代入
            data = [""*7]

        return render_template(
            'shiftform.html',
            week = list('月火水木金土日'),
            nextweek = list('月火水木金土日'),
            data = data,
            user = user,
        )
from .models import FinalShift
@main.route('/shift', methods=['GET'])
@login_required
def shift():
    data = []
    for i in range(7):
        shifts = db.session.query(FinalShift).filter(FinalShift.dayofweek == i, FinalShift.begin != 'x').all()
        shifts_data = []
        for shift in shifts:
            shift_data = {
                'id': shift.id,
                'dayofweek': shift.dayofweek,
                'name': shift.name,
                'begin': shift.begin,
            }
            shifts_data.append(shift_data)
        data.append(shifts_data)
    # return json_data[0][0]
    return render_template(
        "shift.html",
        data = data,
        week = list('月火水木金土日'),
    )
