"""
This module implements instance of login web form
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Email, DataRequired


class LoginForm(FlaskForm):
    """
    Custom FlaskForm object for login form.
    """
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Sign in")
