"""
This module implements instance of register department web form
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from src.rest.api_controllers import DepartmentApiController


class RegisterDepartmentForm(FlaskForm):
    """
    Custom FlaskForm object for register department form.
    """
    name = StringField("Department name", validators=[DataRequired()])
    submit = SubmitField("Create Department")

    def validate_name(self, name):
        """
        validator for department name field
        :param name: department name string field
        :raise ValidationError: if input name already existed in database
        """
        departments = DepartmentApiController.get_all_departments()
        names = [department["name"] for department in departments]
        if name.data in names:
            raise ValidationError("Department with this name is already exists")
