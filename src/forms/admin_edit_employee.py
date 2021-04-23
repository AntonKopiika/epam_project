from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, ValidationError


class AdminEditProfileForm(FlaskForm):
    department = SelectField("Department", choices=[])
    position = StringField("Position", validators=[DataRequired()])
    salary = IntegerField("Salary", validators=[DataRequired()])
    is_admin = BooleanField("Promote to admin")
    submit = SubmitField("Edit Profile")

    def validate_salary(self, salary):
        if salary.data < 0:
            raise ValidationError("Salary must be more than 0.")

