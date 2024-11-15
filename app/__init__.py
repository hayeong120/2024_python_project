import os
from flask import Flask
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Flask 앱을 생성하고 templates 및 static 폴더 경로 명시
app = Flask(__name__, template_folder='../templates', static_folder='../static')

# MySQL 설정
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DATABASE'] = 'Dodam_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

from app import routes
