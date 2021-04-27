import uuid

from sqlalchemy.orm import backref

from src import db


class Department(db.Model):
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
        return f"Department(id: {self.id}, name: {self.name}, employees:{self.employees})"

