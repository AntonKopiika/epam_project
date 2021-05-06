from datetime import datetime
from typing import List

from sqlalchemy import or_, and_
from sqlalchemy.orm import selectinload
from werkzeug.security import generate_password_hash
from src.models.department import Department
from src import db
from src.models.employee import Employee
from src.schemas.department import DepartmentSchema


def get_all_departments() -> List[Department]:
    return db.session.query(Department).options(selectinload(Department.employees)).all()


def get_department_by_id(id: str) -> Department:
    return db.session.query(Department).filter_by(id=int(id)).first()


def get_department_by_uuid(uuid: str) -> Department:
    return db.session.query(Department).filter_by(uuid=uuid).first()


def add_department(department: Department):
    db.session.add(department)
    db.session.commit()


def update_department(department: Department, uuid: str) -> None:
    db.session.query(Department).filter_by(uuid=uuid).update(
        dict(name=department.name)
    )
    db.session.commit()


def alter_department(department: Department, updated_json: dict) -> None:
    name = updated_json.get("name")
    if name:
        department.name = name
    db.session.add(department)
    db.session.commit()


def delete_department(department: Department) -> None:
    db.session.delete(department)
    db.session.commit()


def get_all_employees() -> List[Employee]:
    return db.session.query(Employee).options(selectinload(Employee.department)).all()


def search_employees(name, department_id, start_date, end_date):
    base_query = db.session.query(Employee)
    if name:
        base_query = base_query.filter(or_(Employee.first_name.like(f"%{name}%"), Employee.last_name.like(f"%{name}%")))
    if department_id:
        base_query = base_query.filter(Employee.department_id == department_id)
    if start_date != "None":
        base_query = base_query.filter(and_(Employee.birthday >= start_date, Employee.birthday <= end_date))
    employees = base_query.all()
    return employees


def get_employee_by_id(id: str) -> Employee:
    return db.session.query(Employee).filter_by(uuid=int(id)).first()


def get_employee_by_uuid(uuid: str) -> Employee:
    return db.session.query(Employee).filter_by(uuid=uuid).first()


def get_employee_by_email(email: str) -> Employee:
    return db.session.query(Employee).filter_by(email=email).first()


def add_employee(employee: Employee):
    db.session.add(employee)
    db.session.commit()


def update_employee(employee: Employee, uuid: str) -> None:
    db.session.query(Employee).filter_by(uuid=uuid).update(
        dict(first_name=employee.first_name, last_name=employee.last_name, birthday=employee.birthday,
             position=employee.position, salary=employee.salary, is_admin=employee.is_admin, email=employee.email,
             password=employee.password)
    )
    db.session.commit()


def alter_employee(employee: Employee, updated_json: dict) -> None:
    first_name = updated_json.get("first_name")
    last_name = updated_json.get("last_name")
    birthday = updated_json.get("birthday")
    position = updated_json.get("position")
    salary = updated_json.get("salary")
    is_admin = updated_json.get("is_admin")
    email = updated_json.get("email")
    password = updated_json.get("password")
    department = updated_json.get("department")
    if first_name:
        employee.first_name = first_name
    if last_name:
        employee.last_name = last_name
    if birthday:
        employee.birthday = datetime.strptime(birthday, '%Y-%m-%d')
    if position:
        employee.position = position
    if salary:
        employee.salary = salary
    if is_admin is not None:
        employee.is_admin = is_admin
    if email:
        employee.email = email
    if password:
        employee.password = generate_password_hash(password)
    if department:
        department_schema = DepartmentSchema()
        employee.department = department_schema.load(department, session=db.session)
    db.session.add(employee)
    db.session.commit()


def delete_employee(employee: Employee) -> None:
    db.session.delete(employee)
    db.session.commit()
