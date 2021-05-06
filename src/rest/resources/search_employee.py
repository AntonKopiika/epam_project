from urllib.parse import parse_qs
import src.service.database_queries as service
from flask_restful import Resource
from src.rest.resources.auth import check_authorisation
from src.schemas.employee import EmployeeSchema


class SearchEmployeeApi(Resource):
    employee_schema = EmployeeSchema()

    @check_authorisation
    def get(self, search_query):
        params = parse_qs(search_query)
        department_id = int(params["department"][0]) if params.get("department") else False
        name = params["name"][0] if params.get("name") else False
        start_date = params["start_date"][0] if params.get("start_date") else False
        end_date = params["end_date"][0] if params.get("end_date") else False
        employees = service.search_employees(name, department_id, start_date, end_date)
        return self.employee_schema.dump(employees, many=True), 200
