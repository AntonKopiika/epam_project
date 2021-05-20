"""
This module implements controllers for api requests
"""
import requests
from src.rest.resources.wrappers import handle_errors
from requests.auth import HTTPBasicAuth
from config import Config


class StatisticApiController:
    """
    Controller class for StatisticApi
    """

    @staticmethod
    @handle_errors(correct_response=200, error_code=500)
    def get_department_statistics(uuid):
        """
        method to call get request from StatisticApi
        :param uuid: department uuid
        :return: request json with department statistics
        """
        return requests.get(f"https://flasktestproject2.herokuapp.com/api/department/statistics/{uuid}",
                            auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))


class DepartmentApiController:
    """
    Controller class for DepartmentApi
    """

    @staticmethod
    @handle_errors(correct_response=200, error_code=500)
    def get_all_departments():
        """
        method to get all departments from DepartmentApi
        :return: request json with departments data
        """
        return requests.get("https://flasktestproject2.herokuapp.com/api/department/",
                            auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))

    @staticmethod
    @handle_errors(correct_response=200, error_code=404)
    def get_department_by_uuid(uuid):
        """
        method to get department by uuid from DepartmentApi
        :param uuid: department uuid
        :return: request json with department data
        """
        return requests.get(f"https://flasktestproject2.herokuapp.com/api/department/{uuid}",
                            auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))

    @staticmethod
    def post_department(name):
        """
        method to post department data to DepartmentApi
        :param name: department name
        :return: request response
        """
        json = {"name": name}
        return requests.post("https://flasktestproject2.herokuapp.com/api/department/", json=json,
                             auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))

    @staticmethod
    def put_department(uuid, name):
        """
        method to put department data to DepartmentApi
        :param name: department name
        :param uuid: department uuid
        :return: request response
        """
        json = {"name": name}
        return requests.put(f"https://flasktestproject2.herokuapp.com/api/department/{uuid}", json=json,
                            auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))

    @staticmethod
    def patch_department(uuid, name):
        """
        method to put department data to DepartmentApi
        :param name: department name
        :param uuid: department uuid
        :return: request response
        """
        json = {"name": name}
        return requests.patch(f"https://flasktestproject2.herokuapp.com/api/department/{uuid}", json=json,
                              auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))

    @staticmethod
    def delete_department(uuid):
        """
        method to delete department data from DepartmentApi
        :param uuid: department uuid
        :return: request response
        """
        return requests.delete(f"https://flasktestproject2.herokuapp.com/api/department/{uuid}",
                               auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))


class EmployeeApiController:
    """
    Controller class for EmployeeApi
    """

    @staticmethod
    @handle_errors(correct_response=200, error_code=500)
    def get_all_employees():
        """
        method to get all employees from EmployeeApi
        :return: request json with employees data
        """
        return requests.get("https://flasktestproject2.herokuapp.com/api/employee/",
                            auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))

    @staticmethod
    @handle_errors(correct_response=200, error_code=404)
    def get_employee_by_uuid(uuid):
        """
        method to get employee by uuid from EmployeeApi
        :param uuid: employee uuid
        :return: request json with employee data
        """
        return requests.get(f"https://flasktestproject2.herokuapp.com/api/employee/{uuid}",
                            auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))

    @staticmethod
    def post_employee(first_name, last_name, birthday, position, salary, is_admin, email, password, department):
        """
        method to post employee data to EmployeeApi
        :param first_name: employee's firstname
        :param last_name: employee's lastname
        :param birthday: employee's birthday
        :param position: employee's position
        :param salary: employee's salary
        :param is_admin: employee's is_admin
        :param email: employee's email
        :param password: employee's password
        :param department: employee's department
        :return: request response
        """
        json = {'position': position, 'is_admin': is_admin, 'birthday': birthday.strftime("%Y-%m-%d"),
                'department': {'id': department["id"], 'name': department["name"], 'uuid': department["uuid"]},
                'password': password, 'last_name': last_name, 'salary': salary, 'first_name': first_name,
                'email': email}

        return requests.post("https://flasktestproject2.herokuapp.com/api/employee/", json=json,
                             auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))

    @staticmethod
    def put_employee(uuid, first_name, last_name, birthday, position, salary, is_admin, email, password, department):
        """
        method to put employee data to EmployeeApi
        :param uuid: employee's uuid
        :param first_name: employee's firstname
        :param last_name: employee's lastname
        :param birthday: employee's birthday
        :param position: employee's position
        :param salary: employee's salary
        :param is_admin: employee's is_admin
        :param email: employee's email
        :param password: employee's password
        :param department: employee's department
        :return: request response
        """
        json = {'position': position, 'is_admin': is_admin, 'birthday': birthday.strftime("%Y-%m-%d"),
                'department': {'id': department["id"], 'name': department["name"], 'uuid': department["uuid"]},
                'password': password, 'last_name': last_name, 'salary': salary, 'first_name': first_name,
                'email': email}
        return requests.put(f"https://flasktestproject2.herokuapp.com/api/employee/{uuid}", json=json,
                            auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))

    @staticmethod
    def patch_employee(uuid, first_name=None, last_name=None, birthday=None, position=None, salary=None, is_admin=None,
                       email=None, password=None, department=None):
        """
        method to patch employee data to EmployeeApi
        :param uuid: employee's uuid
        :param first_name: employee's firstname
        :param last_name: employee's lastname
        :param birthday: employee's birthday
        :param position: employee's position
        :param salary: employee's salary
        :param is_admin: employee's is_admin
        :param email: employee's email
        :param password: employee's password
        :param department: employee's department
        :return: request response
        """
        json = {'position': position, 'is_admin': is_admin,
                'birthday': birthday.strftime("%Y-%m-%d") if birthday is not None else None,
                'department': {'id': department["id"], 'name': department["name"],
                               'uuid': department["uuid"]} if department is not None else None,
                'password': password, 'last_name': last_name, 'salary': salary, 'first_name': first_name,
                'email': email}
        return requests.patch(f"https://flasktestproject2.herokuapp.com/api/employee/{uuid}", json=json,
                              auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))

    @staticmethod
    def delete_employee(uuid):
        """
        method to delete employee by uuid from EmployeeApi
        :param uuid: employee uuid
        :return: request response
        """
        return requests.delete(f"https://flasktestproject2.herokuapp.com/api/employee/{uuid}",
                               auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD))


class SearchEmployeeApiController:
    """
    Controller class for SearchEmployeeApi
    """

    @staticmethod
    def search_employees(name, department_id, start, end):
        """
        method to get all employees from SearchEmployeeApi which matches params
        :param name: part of employee's name or lastname
        :param department_id: department id
        :param start: first day of searching
        :param end: last day of searching
        :return: request json with employees
        """
        return requests.get(
            f"https://flasktestproject2.herokuapp.com/api/search/name={name}&department={department_id}&start_date={start}&end_date={end}",
            auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME, Config.API_AUTHORISATION_PASSWORD)).json()

    @staticmethod
    def search_employee_by_email(email):
        """
        method to get employee from SearchEmployeeApi by email
        :param email: employee's email
        :return: request json with employees
        """
        return requests.get(f"https://flasktestproject2.herokuapp.com/api/search/email={email}",
                            auth=HTTPBasicAuth(Config.API_AUTHORISATION_USERNAME,
                                               Config.API_AUTHORISATION_PASSWORD)).json()
