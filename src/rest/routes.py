from flask import request
import src.service.database_queries as service
from flask_restful import Resource

from src import api

BASE_API_URL = "/api"


class Smoke(Resource):
    def get(self):
        return {'message': "OK"}, 200


class DepartmentApi(Resource):
    def get(self, uuid=None):
        if uuid is None:
            departments = service.get_all_departments()
            return [d.to_dict() for d in departments], 200
        department = service.get_department_by_uuid(uuid)
        if not department:
            return "", 404
        return department.to_dict(), 200

    def post(self):
        department_json = request.json
        if not department_json:
            return {"message": "Wrong data"}, 400
        try:
            service.add_department(department_json)
        except (ValueError, KeyError):
            return {"message": "wrong data"}, 400
        return {"message": "created successfully"}, 201

    def patch(self, uuid):
        department = service.get_department_by_uuid(uuid)
        if not department:
            return "", 404
        department_json = request.json
        if not department_json:
            return {"message": "Wrong data"}, 400
        service.alter_department(department, department_json)
        return {"message": "updated successfully"}, 200

    def put(self, uuid):
        department_json = request.json
        if not department_json:
            return {"message": "Wrong data"}, 400
        try:
            service.update_department(department_json, uuid)
        except (ValueError, KeyError):
            return {"message": "wrong data"}, 400
        return {"message": "updated successfully"}, 200

    def delete(self, uuid):
        department = service.get_department_by_uuid(uuid)
        if not department:
            return "", 404
        service.delete_department(department)
        return {"message": "deleted successfully"}, 204


class Employee(Resource):
    pass


api.add_resource(Smoke, f'{BASE_API_URL}/smoke', strict_slashes=False)
api.add_resource(DepartmentApi, f"{BASE_API_URL}/department", f"{BASE_API_URL}/department/<uuid>",
                 strict_slashes=False)
