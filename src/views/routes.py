import requests

from src import app
from flask import render_template, flash, redirect, url_for
from src.forms.login import LoginForm
from src.forms.register import RegisterForm
from flask_login import login_user, current_user, logout_user
import src.service.database_queries as service
from src.rest.request import post_employee
from src.utils.password_utils import random_password
from src.utils.email_utils import send_password
import src.rest.request as api_controller


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Home")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        employee = service.get_employee_by_email(form.email.data)
        if employee is None or not employee.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(employee, remember=form.remember.data)
        flash(f"Login request for {form.email.data}")
        return redirect(url_for("index"))
    return render_template("login.html", form=form, title="Sign in")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    form.department.choices = [(dep.id, dep.name) for dep in service.get_all_departments()]
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        salary = form.salary.data
        position = form.position.data
        birthday = form.birthday.data
        department = service.get_department_by_id(form.department.data)
        password = random_password()
        email = form.email.data
        is_admin = form.is_admin.data
        post_employee(first_name=firstname, last_name=lastname, salary=salary, position=position, is_admin=is_admin,
                      email=email, password=password, department=department, birthday=birthday)
        send_password(email, password)
        flash(f"Register request for {form.firstname.data} {form.lastname.data} {form.department.data}")
        return redirect("index")
    return render_template("register.html", form=form, title="Register")


@app.route("/department")
@app.route("/department/<uuid>")
def department(uuid=None):
    if not uuid:
        departments = api_controller.get_all_departments()
    else:
        departments = [api_controller.get_department_by_uuid(uuid)]
    return render_template("department.html", title="Department", departments=departments)


@app.route("/employee")
@app.route("/employee/<uuid>")
def employee(uuid=None):
    if not uuid:
        employees = api_controller.get_all_employees()
    else:
        employees = [api_controller.get_employee_by_uuid(uuid)]
    return render_template("employee.html", title="Employee", employees=employees)


@app.route("/about")
def about():
    return render_template("about.html", title="About")
