"""
This module implements response for department requests
"""
from flask import request
from marshmallow import ValidationError
import src.service.database_queries as service
from flask_restful import Resource
from src import db
from src.rest.resources.wrappers import check_authorisation
from src.schemas.department import DepartmentSchema


class DepartmentApi(Resource):
    """
    Class for department restfull resource
    """
    department_schema = DepartmentSchema()

    @check_authorisation
    def get(self, uuid=None):
        """
        get method for department request
        :param uuid: optional parameter uses for getting department by uuid
        :return: departments data in json
        """
        if uuid is None:
            departments = service.get_all_departments()
            return self.department_schema.dump(departments, many=True), 200
        department = service.get_department_by_uuid(uuid)
        if not department:
            return "", 404
        return self.department_schema.dump(department), 200

    @check_authorisation
    def post(self):
        """
        post method for department request
        :return: created department data in json
        """
        try:
            department = self.department_schema.load(request.json, session=db.session)
        except ValidationError as err:
            return {"message": str(err)}, 400
        service.add_department(department)
        return self.department_schema.dump(department), 201

    @check_authorisation
    def put(self, uuid):
        """
        put method for department request
        :param uuid: uuid of department you want to change
        :return: changed department data in json
        """
        department = service.get_department_by_uuid(uuid)
        if not department:
            return "", 404
        try:
            department = self.department_schema.load(request.json, session=db.session)
        except ValidationError as err:
            return {"message": str(err)}, 400
        service.update_department(department, uuid)
        return self.department_schema.dump(department), 200

    @check_authorisation
    def patch(self, uuid):
        """
        put method for department request
        :param uuid: uuid of department you want to change
        :return: changed department data in json
        """
        department = service.get_department_by_uuid(uuid)
        if not department:
            return "", 404
        update_json = request.json
        if not update_json:
            return {"message": "nothing to update"}, 400
        service.alter_department(department, update_json)
        return self.department_schema.dump(department), 200

    @check_authorisation
    def delete(self, uuid):
        """
        delete method for department request
        :param uuid: uuid of department you want to delete
        :return: request response
        """
        department = service.get_department_by_uuid(uuid)
        if not department:
            return "", 404
        service.delete_department(department)
        return {"message": "deleted successfully"}, 204
