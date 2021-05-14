"""
This module store wrappers for rest api
"""
from functools import wraps
from flask import request, abort
from config import Config


def handle_errors(correct_response, error_code=404):
    """
    wrapper for checking correct response of api
    :param correct_response: expected response status code
    :param error_code: status, returned if response isn't correct
    :return: request json if response status code is correct, else return with error_code
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = func(*args, **kwargs)
            if request.status_code == correct_response:
                return request.json()
            return abort(error_code)

        return wrapper

    return decorator


def check_authorisation(func):
    """
    wrapper for checking authorisation for api
    :param func: api request function
    :return: not authorised method, if there are no authorisation, else function result
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.authorization:
            username = request.authorization.username
            password = request.authorization.password
            if username == Config.API_AUTHORISATION_USERNAME and password == Config.API_AUTHORISATION_PASSWORD:
                return func(*args, **kwargs)
        return {"message": "Not authorised"}, 401

    return wrapper
