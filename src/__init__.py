from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__, template_folder="templates")
app.config.from_object(Config)
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from src.rest import routes
from src.views import routes
from .models import department
