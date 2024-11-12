from flask import Flask

app = Flask(__name__, template_folder='../templates')  # templates 폴더 경로 명시

from app import routes 