"""
This module implements instance of edit employee profile web form
"""
from datetime import date
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, PasswordField
from wtforms.validators import Email, DataRequired, ValidationError
from src.rest.api_controllers import EmployeeApiController


class EditProfileForm(FlaskForm):
    """
    Custom FlaskForm object for edit employee profile form
    """
    firstname = StringField("First name", validators=[DataRequired()])
    lastname = StringField("Last name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    birthday = DateField("Birthday (like 2000-01-01)", format='%Y-%m-%d', validators=[DataRequired()])
    password = PasswordField("Password")
    confirm_password = PasswordField("Confirm password")
    submit = SubmitField("Edit Profile")

    def validate_birthday(self, birthday):
        """
        validator for birthday field
        :param birthday: birthday date field
        :raise ValidationError: if input date is bigger than today
        """
        if birthday.data > date.today():
            raise ValidationError("Wrong date")

    def validate_email(self, email):
        """
        validator for email field
        :param email: email string field
        :raise ValidationError: if input email already existed in database
        """
        employees = EmployeeApiController.get_all_employees()
        emails = [employee["email"] for employee in employees]
        if email.data in emails and current_user.email != email.data:
            raise ValidationError("This email is already exists")

    def validate_password(self, password):
        """
        validator for password field
        :param password: password field
        :raise ValidationError: if password not entered while confirm password is entered
        """
        if self.confirm_password.data == "" and password.data != "":
            raise ValidationError("Enter password before confirmation")

    def validate_confirm_password(self, confirm_password):
        """
        validator for confirm password field
        :param confirm_password: confirm password field
        :raise ValidationError: if confirm password not entered while password is entered or they doesn't match
        """
        if self.password.data != "" and confirm_password.data == "":
            raise ValidationError("Confirm password")
        if self.password.data != confirm_password.data:
            raise ValidationError("Passwords doesn't match")
