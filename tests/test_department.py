import http
import json
from base64 import b64encode
from dataclasses import dataclass
from datetime import date
from unittest.mock import patch

from config import Config
from src import app
from tests.test_employee import TestEmployee

credentials = b64encode(f"{Config.API_AUTHORISATION_USERNAME}:{Config.API_AUTHORISATION_PASSWORD}".encode()).decode(
    'utf-8')
header = {"Authorization": f"Basic {credentials}"}
uuid = ""
client = app.test_client()

test_employee = TestEmployee()
test_employee.birthday = date(2000, 10, 10)


@dataclass
class TestDepartment:
    name = "some department"
    employees = [test_employee]


def test_get_departments_without_authorisation():
    response = client.get("/api/department")

    assert response.status_code == http.HTTPStatus.UNAUTHORIZED


def test_get_departments_with_db():
    response = client.get("/api/department/", headers=header)

    assert response.status_code == http.HTTPStatus.OK


def test_get_departments_mock_db():
    with patch("src.service.database_queries.get_all_departments", autospec=True,
               return_value=[]) as mock_get_departments:
        response = client.get("/api/department/", headers=header)

        mock_get_departments.assert_called_once()
        assert response.status_code == http.HTTPStatus.OK
        assert len(response.json) == 0


def test_post_department_with_db():
    data = {
        "name": "test department"
    }
    response = client.post("/api/department/", headers=header, content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.CREATED
    assert response.json["name"] == "test department"
    global uuid
    uuid = response.json["uuid"]


def test_post_no_data_department_with_db():
    data = {}
    response = client.post("/api/department/", headers=header, content_type="application/json", data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_post_department_mock_db():
    with patch("src.service.database_queries.add_department", autospec=True) as mock_add_department:
        data = {
            "name": "test department"
        }
        response = client.post("/api/department/", headers=header, content_type="application/json",
                               data=json.dumps(data))

        mock_add_department.assert_called_once()


def test_get_department_with_db():
    response = client.get(f"/api/department/{uuid}", headers=header)

    assert response.status_code == http.HTTPStatus.OK


def test_get_department_mock_db():
    with patch("src.service.database_queries.get_department_by_uuid", autospec=True,
               return_value=TestDepartment()) as mock_get_department:
        response = client.get("/api/department/1", headers=header)
        mock_get_department.assert_called_once()


def test_get_not_found_department_with_db():
    response = client.get(f"/api/department/1", headers=header)

    assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_put_department_with_db():
    data = {
        "name": "some department"
    }
    response = client.put(f"/api/department/{uuid}", headers=header, content_type="application/json",
                          data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.OK
    assert response.json["name"] == "some department"


def test_put_department_mock_db():
    with patch("src.service.database_queries.update_department", autospec=True) as mock_update_department, \
            patch("src.service.database_queries.get_department_by_uuid", autospec=True,
                  return_value=TestDepartment()) as mock_get_department:
        data = {
            "name": "some department"
        }
        response = client.put("/api/department/1", headers=header, content_type="application/json",
                              data=json.dumps(data))

        mock_get_department.assert_called_once()
        mock_update_department.assert_called_once()


def test_put_not_found_department_mock_db():
    with patch("src.service.database_queries.get_department_by_uuid", autospec=True,
               return_value=None) as mock_get_department:
        data = {
            "name": "some department"
        }
        response = client.put("/api/department/1", headers=header, content_type="application/json",
                              data=json.dumps(data))

        mock_get_department.assert_called_once()
        assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_put_validation_department_mock_db():
    with patch("src.service.database_queries.get_department_by_uuid", autospec=True,
               return_value=TestDepartment()) as mock_get_department:
        data = {
            "name": "some department",
            "error_parameter": "not_validated"
        }
        response = client.put("/api/department/1", headers=header, content_type="application/json",
                              data=json.dumps(data))

        mock_get_department.assert_called_once()
        assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_patch_department_with_db():
    data = {
        "name": "test department"
    }
    response = client.patch(f"/api/department/{uuid}", headers=header, content_type="application/json",
                            data=json.dumps(data))

    assert response.status_code == http.HTTPStatus.OK
    assert response.json["name"] == "test department"


def test_patch_department_mock_db():
    with patch("src.service.database_queries.alter_department", autospec=True) as mock_alter_department, \
            patch("src.service.database_queries.get_department_by_uuid", autospec=True,
                  return_value=TestDepartment()) as mock_get_department:
        data = {
            "name": "some department"
        }
        response = client.patch(f"/api/department/1", headers=header, content_type="application/json",
                                data=json.dumps(data))
        mock_get_department.assert_called_once()
        mock_alter_department.assert_called_once()


def test_patch_department_not_found_mock_db():
    with patch("src.service.database_queries.get_department_by_uuid", autospec=True,
               return_value=None) as mock_get_department:
        data = {
            "name": "some department"
        }
        response = client.patch(f"/api/department/1", headers=header, content_type="application/json",
                                data=json.dumps(data))
        mock_get_department.assert_called_once()
        assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_patch_department_no_data_mock_db():
    with patch("src.service.database_queries.get_department_by_uuid", autospec=True,
               return_value=TestDepartment()) as mock_get_department:
        data = {}
        response = client.patch(f"/api/department/1", headers=header, content_type="application/json",
                                data=json.dumps(data))
        mock_get_department.assert_called_once()
        assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_get_department_statistic_with_db():
    response = client.get(f"/api/department/statistics/{uuid}", headers=header)

    assert response.status_code == http.HTTPStatus.OK
    assert response.json["employees"] == 0


def test_get_not_found_department_statistic_mock_db():
    with patch("src.service.database_queries.get_department_by_uuid", autospec=True,
               return_value=None) as mock_get_department:
        response = client.get(f"/api/department/statistics/{uuid}", headers=header)

        mock_get_department.assert_called_once()
        assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_get_department_statistic_mock_db():
    with patch("src.service.database_queries.get_department_by_uuid", autospec=True,
               return_value=TestDepartment()) as mock_get_department:
        response = client.get(f"/api/department/statistics/{uuid}", headers=header)

        assert response.status_code == http.HTTPStatus.OK
        assert response.json["avg_salary"] == test_employee.salary


def test_delete_department_with_db():
    response = client.delete(f"/api/department/{uuid}", headers=header)
    assert response.status_code == http.HTTPStatus.NO_CONTENT


def test_delete_department_mock_db():
    with patch("src.service.database_queries.delete_department", autospec=True) as mock_delete_department, \
            patch("src.service.database_queries.get_department_by_uuid", autospec=True,
                  return_value=TestDepartment()) as mock_get_department:
        response = client.delete(f"/api/department/1", headers=header)
        mock_get_department.assert_called_once()
        mock_delete_department.assert_called_once()


def test_delete_not_found_department_mock_db():
    with patch("src.service.database_queries.get_department_by_uuid", autospec=True,
               return_value=None) as mock_get_department:
        response = client.delete(f"/api/department/1", headers=header)
        mock_get_department.assert_called_once()
        assert response.status_code == http.HTTPStatus.NOT_FOUND
