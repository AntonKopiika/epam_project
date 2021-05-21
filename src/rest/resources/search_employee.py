"""
This module implements response for search requests
"""
from urllib.parse import parse_qs
import src.service.database_queries as service
from flask_restful import Resource
from src.rest.resources.wrappers import check_authorisation
from src.schemas.employee import EmployeeSchema
from datetime import date

class SearchEmployeeApi(Resource):
    """
    Class for search restfull resource
    """
    employee_schema = EmployeeSchema()

    @check_authorisation
    def get(self, search_query):
        """
        get method for search request
        :param search_query: search query with parameters
        :return: employees data in json, if such employees exists
        """
        params = parse_qs(search_query)
        if "email" in params.keys():
            employee = service.get_employee_by_email(params["email"][0])
            return self.employee_schema.dump(employee), 200
        department_id = int(params["department"][0]) if params.get("department") else False
        name = params["name"][0] if params.get("name") else False
        start_date = params["start_date"][0] if params.get("start_date") else False
        end_date = params["end_date"][0] if params.get("end_date") else date.today()
        employees = service.search_employees(name, department_id, start_date, end_date)
        return self.employee_schema.dump(employees, many=True), 200
