import requests

from src.schemas.employee import EmployeeSchema

employee_schema = EmployeeSchema()


def post_employee(first_name, last_name, birthday, position, salary, is_admin, email, password, department):
    json = {'position': position, 'is_admin': is_admin, 'birthday': birthday.strftime("%Y-%m-%d"),
            'department': {'id': department.id, 'name': department.name, 'uuid': department.uuid},
            'password': password, 'last_name': last_name, 'salary': salary, 'first_name': first_name, 'email': email}

    x = requests.post("http://127.0.0.1:5000/api/employee/", json=json)


def get_all_departments():
    request = requests.get("http://127.0.0.1:5000/api/department/")
    departments = request.json()
    return departments


def get_department_by_uuid(uuid):
    request = requests.get(f"http://127.0.0.1:5000/api/department/{uuid}")
    department = request.json()
    return department


def get_all_employees():
    request = requests.get("http://127.0.0.1:5000/api/employee/")
    employees = request.json()
    return employees


def get_employee_by_uuid(uuid):
    request = requests.get(f"http://127.0.0.1:5000/api/employee/{uuid}")
    employee = request.json()
    return employee
