import requests

from src import app
from flask import render_template, flash, redirect, url_for
from src.forms.login import LoginForm
from src.forms.register import RegisterForm
from flask_login import login_user, current_user, logout_user
import src.service.database_queries as service


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
    if form.validate_on_submit():
        flash(f"Register request for {form.firstname.data} {form.lastname.data} {form.birthday.data}")
        return redirect("index")
    return render_template("register.html", form=form, title="Register")


@app.route("/department")
@app.route("/department/<uuid>")
def department(uuid=None):
    if not uuid:
        request = requests.get("http://127.0.0.1:5000/api/department/")
        departments = request.json()
    else:
        request = requests.get(f"http://127.0.0.1:5000/api/department/{uuid}")
        departments = [request.json()]
    return render_template("department.html", title="Department", departments=departments)


@app.route("/employee")
@app.route("/employee/<uuid>")
def employee(uuid=None):
    if not uuid:
        request = requests.get("http://127.0.0.1:5000/api/employee/")
        employees = request.json()
    else:
        request = requests.get(f"http://127.0.0.1:5000/api/employee/{uuid}")
        employees = [request.json()]
    return render_template("employee.html", title="Employee", employees=employees)


@app.route("/about")
def about():
    return render_template("about.html", title="About")
