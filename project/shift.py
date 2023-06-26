from flask_sqlalchemy import SQLAlchemy
from .models import FinalShift
from . import db
from flask_login import current_user

def recent()-> str:
    recent_shift :str = ""
    data = db.session.query(FinalShift).filter(
        FinalShift.name == current_user.name,
        FinalShift.begin != "x"
    )
    for d in data:
        recent_shift += "<li>"
        recent_shift += d.dayofweek
        recent_shift += "曜日"
        recent_shift += d.begin
        recent_shift += "</li>"
    return recent_shift

# 「入れない」と入力された文字を変換する
def escape(d :str) -> str:
    if (d == "" or d == "x" or d == "X" or d == "×"
        or d == "✖︎" or d == "0"):
        # "x"（小文字エックス）に統一
        return "x"
    else:
        return d