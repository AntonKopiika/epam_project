"""
This module implements instance of department in database
"""
import uuid
from sqlalchemy.orm import backref
from src import db


class Department(db.Model):
    """
        Department object stands for representation data in departments table.
        :param id: id of department in db
        :param name: department name
        :param uuid: uuid of department
        :param employees: employees working in department
    """
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    uuid = db.Column(db.String(36), unique=True)
    employees = db.relationship("Employee", backref=backref("department", uselist=False))

    def __init__(self, name, employees=None):
        self.name = name
        self.employees = employees if employees is not None else []
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        """
        method gives string representation of department

        :return: string with department id, name and employees
        """
        return f"Department(id: {self.id}, name: {self.name}, employees:{self.employees})"

