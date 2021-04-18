import uuid

from src import db


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    position = db.Column(db.String(60), nullable=False)
    salary = db.Column(db.Integer)
    birthday = db.Column(db.Date)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    uuid = db.Column(db.String(36), unique=True)

    def __init__(self, first_name, last_name, position, salary, birthday, department=None):
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.salary = salary
        self.birthday = birthday
        self.department = department if department is not None else ""
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f"Employee(id: {self.id}, fname: {self.first_name}, lname: {self.last_name}, position: {self.position})"
