"""
This module implements rendering login and logout routes
"""
from werkzeug.urls import url_parse
from src import app, db
from flask import render_template, flash, redirect, url_for, request
from src.forms.login import LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from src.schemas.employee import EmployeeSchema
from src.rest.api_controllers import SearchEmployeeApiController


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    method render login page on web app
    :return: login page for authorisation in app
    """
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        employee_schema = EmployeeSchema()
        employee_json = SearchEmployeeApiController.search_employee_by_email(form.email.data)
        if employee_json:
            pswd = employee_json.get("password")
            employee = employee_schema.load(employee_json, session=db.session)
            employee.password = pswd
            if employee and employee.check_password(form.password.data):
                login_user(employee, remember=form.remember.data)
                flash(f"You are successfully logged in")
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != "":
                    next_page = url_for("index")
                return redirect(next_page)
        flash("Invalid username or password")
        return redirect(url_for("login"))
    return render_template("login.html", form=form, title="Sign in")


@app.route("/logout")
@login_required
def logout():
    """
    method logout user from web app
    :return: home page view
    """
    logout_user()
    return redirect(url_for("index"))
