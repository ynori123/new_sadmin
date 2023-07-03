## データベースの初期化
```python
from project import db, create_app, models

app = create_app()

# Flaskアプリケーションコンテキスト内でdb.create_all()を呼び出す
with app.app_context():
    db.create_all()
```

__init__.py のapp.configの変更

dayofweekは月曜日が0,日曜日は6とする。