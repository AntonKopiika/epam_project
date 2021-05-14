"""
This module implements smoke restfull resource
"""
from flask_restful import Resource


class Smoke(Resource):
    """
    Class smoke stands for realisation test request to api
    """
    def get(self):
        """
        Test method for checking workability of api
        :return: OK response if api is working
        """
        return {'message': "OK"}, 200
