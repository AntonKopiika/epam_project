from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

app = Flask(__name__, template_folder="templates")
app.config.from_object(Config)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from src.rest import routes
from src.views import base_routes, department_routes, employee_routes, autorisation_routes, error_routes
from src.models import department, employee
