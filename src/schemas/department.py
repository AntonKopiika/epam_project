"""
This module implements department serialising functionality
"""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from src.models.department import Department


class DepartmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Department
        load_instance = True
        include_fk = True

    employees = Nested("EmployeeSchema", many=True, exclude=("department", "department_id"))
