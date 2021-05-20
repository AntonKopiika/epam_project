"""
This module contains all configuration data for web application
"""
import pathlib

BASE_DIR = pathlib.Path(__file__).parent


class Config:

    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR / "data" / "db.sqlite3")
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://srqfyacrusl0kx0a:piht0q0ka35q5ljh@d3y0lbg7abxmbuoi.chr7pe7iynqr.eu-west-1.rds.amazonaws.com:3306/yiusfnvriil0yduw'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "Nothing"
    EMAIL_ADDRES = "antonkopiika24@gmail.com"
    EMAIL_PASSWORD = "testcompany"
    API_AUTHORISATION_USERNAME = "testuser"
    API_AUTHORISATION_PASSWORD = "12345678"
