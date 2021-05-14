"""
This module contains all configuration data for web application
"""
import pathlib

BASE_DIR = pathlib.Path(__file__).parent


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR / "data" / "db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "Nothing"
    EMAIL_ADDRES = "antonkopiika24@gmail.com"
    EMAIL_PASSWORD = "testcompany"
    API_AUTHORISATION_USERNAME = "testuser"
    API_AUTHORISATION_PASSWORD = "12345678"
