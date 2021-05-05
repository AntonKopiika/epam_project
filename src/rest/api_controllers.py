import requests
from flask_restful import abort
from requests.auth import HTTPBasicAuth

from config import Config


def handle_errors(correct_response, error_code=404):
    def decorator(func):
        def wrapper(*args, **kwargs):
            request = func(*args, **kwargs)
            if request.status_code == correct_response:
                return request.json()
            return abort(error_code)

        return wrapper

    return decorator


class StatisticApiController:
    @staticmethod
    @handle_errors(correct_response=200, error_code=500)
    def get_department_statistics(uuid):
        return requests.get(f"http://127.0.0.1:5000/api/department/statistics/{uuid}",
                            auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))


class DepartmentApiController:
    @staticmethod
    @handle_errors(correct_response=200, error_code=500)
    def get_all_departments():
        return requests.get("http://127.0.0.1:5000/api/department/",
                            auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))

    @staticmethod
    @handle_errors(correct_response=200, error_code=404)
    def get_department_by_uuid(uuid):
        return requests.get(f"http://127.0.0.1:5000/api/department/{uuid}",
                            auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))

    @staticmethod
    def post_department(name):
        json = {"name": name}
        return requests.post("http://127.0.0.1:5000/api/department/", json=json,
                          auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))

    @staticmethod
    def put_department(uuid, name):
        json = {"name": name}
        return requests.put(f"http://127.0.0.1:5000/api/department/{uuid}", json=json,
                         auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))

    @staticmethod
    def patch_department(uuid, name):
        json = {"name": name}
        return requests.patch(f"http://127.0.0.1:5000/api/department/{uuid}", json=json,
                           auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))


    @staticmethod
    def delete_department(uuid):
        return requests.delete(f"http://127.0.0.1:5000/api/department/{uuid}",
                            auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))


class EmployeeApiController:

    @staticmethod
    @handle_errors(correct_response=200, error_code=500)
    def get_all_employees():
        return requests.get("http://127.0.0.1:5000/api/employee/",
                            auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))

    @staticmethod
    @handle_errors(correct_response=200, error_code=404)
    def get_employee_by_uuid(uuid):
        return requests.get(f"http://127.0.0.1:5000/api/employee/{uuid}",
                            auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))

    @staticmethod
    def post_employee(first_name, last_name, birthday, position, salary, is_admin, email, password, department):
        json = {'position': position, 'is_admin': is_admin, 'birthday': birthday.strftime("%Y-%m-%d"),
                'department': {'id': department["id"], 'name': department["name"], 'uuid': department["uuid"]},
                'password': password, 'last_name': last_name, 'salary': salary, 'first_name': first_name,
                'email': email}

        return requests.post("http://127.0.0.1:5000/api/employee/", json=json,
                          auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))

    @staticmethod
    def put_employee(uuid, first_name, last_name, birthday, position, salary, is_admin, email, password, department):
        json = {'position': position, 'is_admin': is_admin, 'birthday': birthday.strftime("%Y-%m-%d"),
                'department': {'id': department["id"], 'name': department["name"], 'uuid': department["uuid"]},
                'password': password, 'last_name': last_name, 'salary': salary, 'first_name': first_name,
                'email': email}
        return requests.put(f"http://127.0.0.1:5000/api/employee/{uuid}", json=json,
                         auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))

    @staticmethod
    def patch_employee(uuid, first_name=None, last_name=None, birthday=None, position=None, salary=None, is_admin=None,
                       email=None, password=None, department=None):
        json = {'position': position, 'is_admin': is_admin,
                'birthday': birthday.strftime("%Y-%m-%d") if birthday is not None else None,
                'department': {'id': department["id"], 'name': department["name"],
                               'uuid': department["uuid"]} if department is not None else None,
                'password': password, 'last_name': last_name, 'salary': salary, 'first_name': first_name,
                'email': email}
        return requests.patch(f"http://127.0.0.1:5000/api/employee/{uuid}", json=json,
                           auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))

    @staticmethod
    def delete_employee(uuid):
        return requests.delete(f"http://127.0.0.1:5000/api/employee/{uuid}",
                            auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))
