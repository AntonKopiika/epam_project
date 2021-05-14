"""
This module implements instance of search employee web form
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, validators
from wtforms.validators import ValidationError


class EmployeeSearchForm(FlaskForm):
    """
    Custom FlaskForm object for searching employees form
    """
    department = SelectField("department")
    name = StringField("Search")
    from_birthday = DateField("Start date", validators=(validators.Optional(),))
    to_birthday = DateField("End date", validators=(validators.Optional(),))
    submit = SubmitField("Search")

    def validate_from_birthday(self, from_birthday):
        """
        validator for from_birthday field
        :param from_birthday: birthday date field
        :raise ValidationError: start date is bigger than end date
        """
        if self.to_birthday.data and from_birthday.data:
            if from_birthday.data > self.to_birthday.data:
                raise ValidationError("Start date is bigger than end date")
