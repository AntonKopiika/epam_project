import http
import json
from base64 import b64encode
from dataclasses import dataclass
from unittest.mock import patch

from config import Config
from src import app

credentials = b64encode(f"{Config.API_AUTHORISATION_USERNAME}:{Config.API_AUTHORISATION_PASSWORD}".encode()).decode(
    'utf-8')
header = {"Authorization": f"Basic {credentials}"}
uuid = ""
client = app.test_client()


@dataclass
class TestEmployee:
    position = "position"
    is_admin = False
    birthday = "2000-01-01"
    last_name = "User"
    salary = 2000
    first_name = "Test"
    email = "test@mail.ru"
    password = "test"


def test_get_employees_without_authorisation():
    response = client.get("/api/employee")
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED


def test_get_employees_with_db():
    response = client.get("/api/employee/", headers=header)

    assert response.status_code == http.HTTPStatus.OK


def test_get_employees_mock_db():
    with patch("src.service.database_queries.get_all_employees", autospec=True,
               return_value=[]) as mock_get_employees:
        response = client.get("/api/employee/", headers=header)
        mock_get_employees.assert_called_once()
        assert len(response.json) == 0


def test_post_employee_with_db():
    data = {'position': "position", 'is_admin': False, 'birthday': "2000-01-01", 'last_name': "User",
            'salary': 2000, 'first_name': "Test", 'email': "test@mail.ru", "password": "test"}
    response = client.post("/api/employee/", headers=header, content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.CREATED
    assert response.json["first_name"] == "Test"
    global uuid
    uuid = response.json["uuid"]


def test_post_wrong_data_employee_with_db():
    data = {"name": "test"}
    response = client.post("/api/employee/", headers=header, content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_post_employee_mock_db():
    with patch("src.service.database_queries.add_employee", autospec=True) as mock_add_employee:
        data = {'position': "position", 'is_admin': False, 'birthday': "2000-01-01", 'last_name': "User",
                'salary': 2000, 'first_name': "Test", 'email': "test@mail.ru", "password": "test"}
        response = client.post("/api/employee/", headers=header, content_type="application/json", data=json.dumps(data))

        mock_add_employee.assert_called_once()


def test_get_employee_with_db():
    response = client.get(f"/api/employee/{uuid}", headers=header)

    assert response.status_code == http.HTTPStatus.OK


def test_get_employee_mock_db():
    with patch("src.service.database_queries.get_employee_by_uuid", autospec=True,
               return_value=TestEmployee()) as mock_get_department:
        response = client.get("/api/employee/1", headers=header)

        mock_get_department.assert_called_once()


def test_get_not_found_employee_with_db():
    response = client.get(f"/api/employee/1", headers=header)

    assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_get_employee_by_email_with_db():
    response = client.get(f"/api/search/email=test@mail.ru", headers=header)

    assert response.status_code == http.HTTPStatus.OK
    assert response.json["first_name"] == "Test"


def test_search_employees_with_db():
    response = client.get(f"/api/search/name=Test&department=0&start_date=None&end_date=None", headers=header)

    assert response.status_code == http.HTTPStatus.OK
    assert len(response.json) != 0


def test_put_employee_with_db():
    data = {'position': "position", 'is_admin': False, 'birthday': "2000-01-01", 'last_name': "User",
            'salary': 2000, 'first_name': "Some", 'email': "test@mail.ru", "password": "test"}
    response = client.put(f"/api/employee/{uuid}", headers=header, content_type="application/json",
                          data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.OK
    assert response.json["first_name"] == "Some"


def test_put_employee_mock_db():
    with patch("src.service.database_queries.update_employee", autospec=True) as mock_update_employee, \
            patch("src.service.database_queries.get_employee_by_uuid", autospec=True,
                  return_value=TestEmployee()) as mock_get_employee:
        data = {'position': "position", 'is_admin': False, 'birthday': "2000-01-01", 'last_name': "User",
                'salary': 2000, 'first_name': "Some", 'email': "test@mail.ru", "password": "test"}
        response = client.put("/api/employee/1", headers=header, content_type="application/json", data=json.dumps(data))

        mock_get_employee.assert_called_once()
        mock_update_employee.assert_called_once()


def test_put_not_found_employee_mock_db():
    with patch("src.service.database_queries.get_employee_by_uuid", autospec=True,
               return_value=None) as mock_get_employee:
        data = {'position': "position", 'is_admin': False, 'birthday': "2000-01-01", 'last_name': "User",
                'salary': 2000, 'first_name': "Some", 'email': "test@mail.ru", "password": "test"}
        response = client.put("/api/employee/1", headers=header, content_type="application/json",
                              data=json.dumps(data))

        mock_get_employee.assert_called_once()
        assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_put_validation_employee_mock_db():
    with patch("src.service.database_queries.get_employee_by_uuid", autospec=True,
               return_value=TestEmployee()) as mock_get_employee:
        data = {'position': "position", 'is_admin': False, 'birthday': "2000-01-01",
                'department': {'id': 1, 'name': "name", 'uuid': "uuid"},
                'password': "password", 'last_name': "last_name", 'salary': 600, 'first_name': "first_name",
                'email': "test@mail.ru", "error": "error"}
        response = client.put("/api/employee/1", headers=header, content_type="application/json",
                              data=json.dumps(data))

        mock_get_employee.assert_called_once()
        assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_patch_employee_with_db():
    data = {
        "first_name": "test"
    }
    response = client.patch(f"/api/employee/{uuid}", headers=header, content_type="application/json",
                            data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.OK
    assert response.json["first_name"] == "test"


def test_patch_employee_mock_db():
    with patch("src.service.database_queries.alter_employee", autospec=True) as mock_alter_employee, \
            patch("src.service.database_queries.get_employee_by_uuid", autospec=True,
                  return_value=TestEmployee()) as mock_get_employee:
        data = {
            "first_name": "test"
        }
        response = client.patch(f"/api/employee/1", headers=header, content_type="application/json",
                                data=json.dumps(data))
        mock_get_employee.assert_called_once()
        mock_alter_employee.assert_called_once()


def test_patch_employee_not_found_mock_db():
    with patch("src.service.database_queries.get_employee_by_uuid", autospec=True,
               return_value=None) as mock_get_employee:
        data = {
            "first_name": "test"
        }
        response = client.patch(f"/api/employee/1", headers=header, content_type="application/json",
                                data=json.dumps(data))
        mock_get_employee.assert_called_once()
        assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_patch_employee_no_data_mock_db():
    with patch("src.service.database_queries.get_employee_by_uuid", autospec=True,
               return_value=TestEmployee()) as mock_get_employee:
        data = {}
        response = client.patch(f"/api/employee/1", headers=header, content_type="application/json",
                                data=json.dumps(data))
        mock_get_employee.assert_called_once()
        assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_delete_employee_with_db():
    response = client.delete(f"/api/employee/{uuid}", headers=header)
    assert response.status_code == http.HTTPStatus.NO_CONTENT


def test_delete_department_mock_db():
    with patch("src.service.database_queries.delete_employee", autospec=True) as mock_delete_employee, \
            patch("src.service.database_queries.get_employee_by_uuid", autospec=True,
                  return_value=TestEmployee()) as mock_get_employee:
        response = client.delete(f"/api/employee/1", headers=header)
        mock_get_employee.assert_called_once()
        mock_delete_employee.assert_called_once()


def test_delete_not_found_employee_mock_db():
    with patch("src.service.database_queries.get_employee_by_uuid", autospec=True,
               return_value=None) as mock_get_employee:
        response = client.delete(f"/api/employee/1", headers=header)
        mock_get_employee.assert_called_once()
        assert response.status_code == http.HTTPStatus.NOT_FOUND
