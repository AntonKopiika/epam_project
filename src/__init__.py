"""
Package stores source files of project
"""
import logging
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from logging.handlers import RotatingFileHandler
import os
from flask_mail import Mail

app = Flask(__name__, template_folder="templates")
app.config.from_object(Config)

if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler('logs/logs.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s: %(message)s in %(pathname)s:%(lineno)d'))
file_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('App startup')

api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'antonkopiika24@gmail.com'  # введите свой адрес электронной почты здесь
app.config['MAIL_DEFAULT_SENDER'] = 'antonkopiika24@gmail.com'  # и здесь
app.config['MAIL_PASSWORD'] = 'testcompany'  # введите пароль
mail = Mail(app)

from src.rest import routes
from src.views import base_routes, department_routes, employee_routes, \
    autorisation_routes, error_routes
from src.models import department, employee
from src.service.population import populate


@app.before_first_request
def setup():
    db.create_all()

