from flask import Flask

# Flask 앱을 생성하고 templates 및 static 폴더 경로 명시
app = Flask(__name__, template_folder='../templates', static_folder='../static')

from app import routes
