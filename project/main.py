from flask import Blueprint,render_template, request
from flask_login import login_required,current_user
from . import db

main = Blueprint('main', __name__)

import datetime
from .shift import recent
@main.route('/')
def index():
    dt :datetime = datetime.datetime.now()
    return render_template(
        'index.html',
        recent = recent(),
        today = dt.date(),
        log = [
            ("2023-02-22", "シフトを更新しました。", "Admin"),
        ]
    )

@main.route('/profile')
@login_required
def profile():

    return render_template('profile.html',name=current_user.name)

from .models import PostedShift
from .shift import escape
@main.route('/shiftform', methods=['GET', 'POST'])
@login_required
def shiftform():
    if request.method == 'POST':
        for i in range(7):
            db.session.add(
                PostedShift(
                    dayofweek = i,
                    name = request.form.get('name'),
                    begin = escape(request.form.get('form'+str(i)))
                )
            )
            db.session.commit()

        return request.form

    elif request.method == 'GET':
        data :list[str] = [""] *7

        return render_template(
            'shiftform.html',
            week = list('月火水木金土日'),
            nextweek = list('月火水木金土日'),
            data = data,
        )
from .models import FinalShift
@main.route('/shift', methods=['GET'])
@login_required
def shift():
    data = []
    for i in range(7):
        data[i] = db.session.query(FinalShift).\
            filter(
                FinalShift.dayofweek==i and 
                FinalShift.begin != 'x'
            ).all()
    return data