"""
This module implements instance of employee in database
"""
import uuid
from flask_login import UserMixin
from src import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash


class Employee(db.Model, UserMixin):
    """
    Employee object stands for representation data in employees table.
    :param first_name: first name of employee
    :param last_name: last name of employee
    :param position: position of employee
    :param salary: salary of employee
    :param birthday: birthday of employee in date type
    :param email: email of employee
    :param password: password for employee account
    :param is_admin: bool parameter for admins only, False by default
    :param department: Department object, in which department employee works, None by default
    """
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    position = db.Column(db.String(60), nullable=False)
    salary = db.Column(db.Integer)
    birthday = db.Column(db.Date)
    is_admin = db.Column(db.Boolean, default=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    uuid = db.Column(db.String(36), unique=True)
    password = db.Column(db.String(120), nullable=False, default="test")

    def __init__(self, first_name, last_name, position, salary, birthday, email, password, is_admin=False,
                 department=None):
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.salary = salary
        self.birthday = birthday
        self.email = email
        self.is_admin = is_admin
        self.password = generate_password_hash(password)
        self.department = department if department is not None else None
        self.uuid = str(uuid.uuid4())

    def check_password(self, password):
        """
        method checks equality of given password with employee's

        :param password: password to compare with employee's password

        :return True if given password hash is equal to password hash of employee
        """
        return check_password_hash(self.password, password)

    def __repr__(self):
        """
        method gives string representation of employee

        :return: string with employee id, firstname, lastname and position
        """
        return f"Employee(id: {self.id}, fname: {self.first_name}, lname: {self.last_name}, position: {self.position})"


@login_manager.user_loader
def load_user(employee_id):
    """
    method gives employee object for current registered employee

    :param employee_id: id of employee in db

    :return: employee object
    """
    return Employee.query.get(employee_id)
