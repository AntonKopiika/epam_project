from werkzeug.security import check_password_hash
from werkzeug.urls import url_parse
from src import app, db
from flask import render_template, flash, redirect, url_for, request
from src.forms.login import LoginForm
from flask_login import login_user, current_user, logout_user, login_required
import src.service.database_queries as service
from src.schemas.employee import EmployeeSchema
from src.rest.api_controllers import SearchEmployeeApiController


@app.route("/login", methods=["GET", "POST"])
def login():
    employee_schema = EmployeeSchema()
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        employee_json = SearchEmployeeApiController.search_employee_by_email(form.email.data)
        pswd = employee_json["password"]
        json = {'id': employee_json['id'], 'position': employee_json["position"], 'is_admin': employee_json["is_admin"],
                'birthday': employee_json["birthday"], 'department': {'id': employee_json["department"]["id"],
                                                                 'name': employee_json["department"]["name"],
                                                                 'uuid': employee_json["department"]["uuid"]},
                'password': employee_json["password"], 'last_name': employee_json["last_name"],
                'salary': employee_json["salary"], 'first_name': employee_json["first_name"],
                'email': employee_json["email"]}
        employee = employee_schema.load(json, session=db.session)
        employee.password = pswd
        if employee is None or not employee.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(employee, remember=form.remember.data)
        flash(f"You are successfully logged in")
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", form=form, title="Sign in")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
