"""
This module implements response for employee requests
"""
from flask import request
from marshmallow import ValidationError
import src.service.database_queries as service
from flask_restful import Resource
from src import db
from src.rest.resources.wrappers import check_authorisation
from src.schemas.employee import EmployeeSchema


class EmployeeApi(Resource):
    """
    Class for employee restfull resource
    """
    employee_schema = EmployeeSchema()

    @check_authorisation
    def get(self, uuid=None):
        """
        get method for employee request
        :param uuid: optional parameter uses for getting employee by uuid
        :return: employees data in json
        """
        if uuid is None:
            employees = service.get_all_employees()
            return self.employee_schema.dump(employees, many=True), 200
        employee = service.get_employee_by_uuid(uuid)
        if not employee:
            return "", 404
        return self.employee_schema.dump(employee), 200

    @check_authorisation
    def post(self):
        """
        post method for employee request
        :return: created employee data in json
        """
        try:
            employee = self.employee_schema.load(request.json, session=db.session)
        except ValidationError as err:
            return {"message": str(err)}, 400
        service.add_employee(employee)
        return self.employee_schema.dump(employee), 201

    @check_authorisation
    def put(self, uuid):
        """
        put method for employee request
        :param uuid: uuid of employee you want to change
        :return: changed employee data in json
        """
        employee = service.get_employee_by_uuid(uuid)
        if not employee:
            return "", 404
        try:
            employee = self.employee_schema.load(request.json, session=db.session)
        except ValidationError as err:
            return {"message": str(err)}, 400
        service.update_employee(employee, uuid)
        return self.employee_schema.dump(employee), 200

    @check_authorisation
    def patch(self, uuid):
        """
        patch method for employee request
        :param uuid: uuid of employee you want to change
        :return: changed employee data in json
        """
        employee = service.get_employee_by_uuid(uuid)
        if not employee:
            return "", 404
        update_json = request.json
        if not update_json:
            return {"message": "nothing to update"}, 400
        service.alter_employee(employee, update_json)
        return self.employee_schema.dump(employee), 200

    @check_authorisation
    def delete(self, uuid):
        """
        delete method for employee request
        :param uuid: uuid of employee you want to delete
        :return: request response
        """
        employee = service.get_employee_by_uuid(uuid)
        if not employee:
            return "", 404
        service.delete_employee(employee)
        return {"message": "deleted successfully"}, 204
