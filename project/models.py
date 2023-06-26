from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

# 提出されたシフト
class PostedShift(db.Model):
    # ユニークID
    id = db.Column(db.Integer, primary_key=True)
    # 曜日（月曜日:0, 日曜日:6）
    dayofweek = db.Column(db.Integer)
    # 名前
    name = db.Column(db.String(1000))
    # 出勤時間
    begin = db.Column(db.String(8))

class FinalShift(db.Model):
    # ユニークID
    id = db.Column(db.Integer, primary_key=True)
    # 曜日（月曜日:0, 日曜日:6）
    dayofweek = db.Column(db.Integer)
    # 名前
    name = db.Column(db.String(1000))
    # 出勤時間
    begin = db.Column(db.String(8))

class Employee(UserMixin, db.Model):
    # ユニークID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # ユーザ名
    username = db.Column(db.String(40), unique=True, nullable=False)
    # パスワード
    password = db.Column(db.String(100), nullable=False)
    # 時給
    wages = db.Column(db.Integer)