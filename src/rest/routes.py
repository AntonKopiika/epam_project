"""
This module stores routes for api resources
"""
from src import api
from src.rest.resources.department import DepartmentApi
from src.rest.resources.employee import EmployeeApi
from src.rest.resources.smoke import Smoke
from src.rest.resources.statistics import Statistics
from src.rest.resources.search_employee import SearchEmployeeApi

BASE_API_URL = "/api"

api.add_resource(Smoke, f'{BASE_API_URL}/smoke', strict_slashes=False)
api.add_resource(DepartmentApi, f"{BASE_API_URL}/department", f"{BASE_API_URL}/department/<uuid>",
                 strict_slashes=False)
api.add_resource(EmployeeApi, f"{BASE_API_URL}/employee", f"{BASE_API_URL}/employee/<uuid>",
                 strict_slashes=False)
api.add_resource(Statistics, f"{BASE_API_URL}/department/statistics/<uuid>", strict_slashes=False)
api.add_resource(SearchEmployeeApi, f"{BASE_API_URL}/search/<search_query>", strict_slashes=False)
