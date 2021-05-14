"""
This module implements employee serialising functionality
"""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from src.models.employee import Employee


class EmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        load_instance = True
        include_fk = True

    department = Nested("DepartmentSchema", many=False, exclude=("employees",))

