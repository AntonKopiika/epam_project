from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from src.rest.api_controllers import DepartmentApiController


class RegisterDepartmentForm(FlaskForm):
    name = StringField("Department name", validators=[DataRequired()])
    submit = SubmitField("Create Department")

    def validate_name(self, name):
        departments = DepartmentApiController.get_all_departments()
        names = [department["name"] for department in departments]
        if name.data in names:
            raise ValidationError("Department with this name is already exists")
