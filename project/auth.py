from flask import Blueprint,render_template, redirect, url_for,request, flash,send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, logout_user
from . import db

auth = Blueprint('auth', __name__)

import os
@auth.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(auth.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )

# ログイン
@auth.route('/login')
def login():
    return render_template('login.html', methods=['GET'])

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('ログイン情報を確認して、もう一度お試しください。')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.shiftform'))

# アカウント登録
@auth.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() 

    if user: 
        flash('そのメールアドレスはすでに登録されています。')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

# ログアウト
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# 管理者ログイン