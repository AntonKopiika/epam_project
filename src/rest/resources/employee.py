from flask import request
from marshmallow import ValidationError

import src.service.database_queries as service
from flask_restful import Resource

from src import db
from src.schemas.employee import EmployeeSchema


class EmployeeApi(Resource):
    employee_schema = EmployeeSchema()

    def get(self, uuid=None):
        if uuid is None:
            employees = service.get_all_employees()
            return self.employee_schema.dump(employees, many=True), 200
        employee = service.get_employee_by_uuid(uuid)
        if not employee:
            return "", 404
        return self.employee_schema.dump(employee), 200

    def post(self):
        try:
            employee = self.employee_schema.load(request.json, session=db.session)
        except ValidationError as err:
            return {"message": err}, 400
        service.add_employee(employee)
        return {"message": "created successfully"}, 201

    def put(self, uuid):
        employee = service.get_employee_by_uuid(uuid)
        if not employee:
            return "", 404
        try:
            employee = self.employee_schema.load(request.json, session=db.session)
        except ValidationError as err:
            return {"message": err}, 400
        service.update_employee(employee, uuid)
        return {"message": "updated successfully"}, 200

    def patch(self, uuid):
        employee = service.get_employee_by_uuid(uuid)
        if not employee:
            return "", 404
        update_json = request.json
        if not update_json:
            return {"message": "nothing to update"}, 404
        service.alter_employee(employee, update_json)
        return {"message": "updated successfully"}, 200

    def delete(self, uuid):
        employee = service.get_employee_by_uuid(uuid)
        if not employee:
            return "", 404
        service.delete_employee(employee)
        return {"message": "deleted successfully"}, 204
