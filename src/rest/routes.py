from src import api
from src.rest.resources.department import DepartmentApi
from src.rest.resources.employee import EmployeeApi
from src.rest.resources.smoke import Smoke

BASE_API_URL = "/api"


api.add_resource(Smoke, f'{BASE_API_URL}/smoke', strict_slashes=False)
api.add_resource(DepartmentApi, f"{BASE_API_URL}/department", f"{BASE_API_URL}/department/<uuid>",
                 strict_slashes=False)
api.add_resource(EmployeeApi, f"{BASE_API_URL}/employee", f"{BASE_API_URL}/employee/<uuid>",
                 strict_slashes=False)
