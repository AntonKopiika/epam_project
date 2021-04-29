from functools import wraps
from flask import request
from config import Config


def check_authorisation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.authorization:
            username = request.authorization.username
            password = request.authorization.password
            if username == Config.API_AUTHORISATION_USERNAME and password == Config.API_AUTHORISATION_PASSWORD:
                return func(*args, **kwargs)
        return {"message": "Not authorised"}, 401

    return wrapper
