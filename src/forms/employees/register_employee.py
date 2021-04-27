from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField, SelectField, BooleanField
from wtforms.validators import Email, DataRequired, ValidationError
from src.rest.api_controllers import EmployeeApiController


class RegisterForm(FlaskForm):
    firstname = StringField("First name", validators=[DataRequired()])
    lastname = StringField("Last name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    birthday = DateField("Birthday (like 2000-01-01)", format='%Y-%m-%d', validators=[DataRequired()])
    department = SelectField("Department", choices=[])
    position = StringField("Position", validators=[DataRequired()])
    salary = IntegerField("Salary", validators=[DataRequired()])
    is_admin = BooleanField("Promote to admin")
    submit = SubmitField("Register")

    def validate_salary(self, salary):
        if salary.data < 0:
            raise ValidationError("Salary must be more than 0.")

    def validate_birthday(self, birthday):
        if birthday.data > date.today():
            raise ValidationError("Wrong date")

    def validate_email(self, email):
        employees = EmployeeApiController.get_all_employees()
        emails = [employee["email"] for employee in employees]
        if email.data in emails:
            raise ValidationError("This email is already exists")
