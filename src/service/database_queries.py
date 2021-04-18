from typing import List

from src.models.department import Department
from src import db


def get_all_departments() -> List[Department]:
    return db.session.query(Department).all()


def get_department_by_uuid(uuid: str) -> Department:
    return db.session.query(Department).filter_by(uuid=uuid).first()


def add_department(department_json: dict):
    department = Department(name=department_json["name"])
    db.session.add(department)
    db.session.commit()


def update_department(department_json: dict, uuid: str) -> None:
    db.session.query(Department).filter_by(uuid=uuid).update(
        dict(name=department_json["name"])
    )
    db.session.commit()


def alter_department(department: Department, department_json: dict) -> None:
    name = department_json.get("name")
    if name:
        department.name = name
    db.session.add(department)
    db.session.commit()


def delete_department(department: Department) -> None:
    db.session.delete(department)
    db.session.commit()
