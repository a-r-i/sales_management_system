# sales_management_system
Salse Management System made with Django

# 動作確認済環境
- Python 3.6.3
- Django 2.1.5
- CentOS Linux release 7.6.1810 (Core)

# 実行手順

1. リポジトリをクローン  
`$ git clone https://github.com/a-r-i/sales_management_system.git`

1. プロジェクトディレクトリに移動  
`$ cd sales_management_system/`

1. 依存パッケージをインストール  
`$ pip install -r requirements.txt`

1. local_settings.pyを作成  
`$ python utility/generate_local_settings.py`

1. データベースにテーブルを作成  
`$ python manage.py migrate`

1. 管理ユーザーを作成。この際に入力したユーザー名とパスワードを控えておく  
`$ python manage.py createsuperuser`

1. 開発用サーバーを起動  
`$ python manage.py runserver`

1. `http://127.0.0.1:8000/login/`にアクセス

1. 6で控えておいたユーザー名とパスワードでログイン