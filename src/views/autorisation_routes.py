from werkzeug.urls import url_parse
from src import app
from flask import render_template, flash, redirect, url_for, request
from src.forms.login import LoginForm
from flask_login import login_user, current_user, logout_user, login_required
import src.service.database_queries as service


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



