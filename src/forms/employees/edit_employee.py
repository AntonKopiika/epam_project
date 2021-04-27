from datetime import date

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, PasswordField
from wtforms.validators import Email, DataRequired, ValidationError
from src.rest.api_controllers import EmployeeApiController


class EditProfileForm(FlaskForm):
    firstname = StringField("First name", validators=[DataRequired()])
    lastname = StringField("Last name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    birthday = DateField("Birthday (like 2000-01-01)", format='%Y-%m-%d', validators=[DataRequired()])
    password = PasswordField("Password")
    confirm_password = PasswordField("Confirm password")
    submit = SubmitField("Edit Profile")

    def validate_birthday(self, birthday):
        if birthday.data > date.today():
            raise ValidationError("Wrong date")

    def validate_email(self, email):
        employees = EmployeeApiController.get_all_employees()
        emails = [employee["email"] for employee in employees]
        if email.data in emails and current_user.email != email.data:
            raise ValidationError("This email is already exists")

    def validate_password(self, password):
        if self.confirm_password.data == "" and password.data != "":
            raise ValidationError("Enter password before confirmation")

    def validate_confirm_password(self, confirm_password):
        if self.password.data != "" and confirm_password.data == "":
            raise ValidationError("Confirm password")
        if self.password.data != confirm_password.data:
            raise ValidationError("Passwords doesn't match")
