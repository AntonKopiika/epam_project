"""
This module implements instance of edit employee profile by admin web form
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, ValidationError


class AdminEditProfileForm(FlaskForm):
    """
    Custom FlaskForm object for edit employee profile by admin form
    """
    department = SelectField("Department", choices=[])
    position = StringField("Position", validators=[DataRequired()])
    salary = IntegerField("Salary", validators=[DataRequired()])
    is_admin = BooleanField("Promote to admin")
    submit = SubmitField("Edit Profile")

    def validate_salary(self, salary):
        """
        validator for salary field
        :param salary: salary integer field
        :raise ValidationError: if input data is below zero
        """
        if salary.data < 0:
            raise ValidationError("Salary must be more than 0.")

