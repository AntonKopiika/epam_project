import uuid

from src import db


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    uuid = db.Column(db.String(36), unique=True)

    def __init__(self, name):
        self.name = name
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f"Department(id: {self.id}, name: {self.name})"

    def to_dict(self):
        return {
            "name": self.name,
            "uuid": self.uuid
        }
