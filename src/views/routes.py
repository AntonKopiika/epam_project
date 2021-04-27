from functools import wraps

from src import app
from flask import render_template, flash, redirect, url_for, request

from src.forms.employees.admin_edit_employee import AdminEditProfileForm
from src.forms.employees.edit_employee import EditProfileForm
from src.forms.login import LoginForm
from src.forms.departments.register_department import RegisterDepartmentForm
from src.forms.employees.register_employee import RegisterForm
from src.forms.departments.edit_department import EditDepartmentForm
from flask_login import login_user, current_user, logout_user, login_required
import src.service.database_queries as service
from src.rest.api_controllers import EmployeeApiController, DepartmentApiController, StatisticApiController
from src.utils.password_utils import random_password
from src.utils.email_utils import send_password


def admins_only(func):
    @wraps(func)
    def admin_wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_admin:
            return func(*args, **kwargs)
        flash(f"Access denied")
        return redirect(url_for("index"))

    return admin_wrapper


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
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register_employee", methods=["GET", "POST"])
@admins_only
@login_required
def register():
    form = RegisterForm()
    form.department.choices = [(dep["uuid"], dep["name"]) for dep in DepartmentApiController.get_all_departments()]
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        salary = form.salary.data
        position = form.position.data
        birthday = form.birthday.data
        department = DepartmentApiController.get_department_by_uuid(form.department.data)
        password = random_password()
        email = form.email.data
        is_admin = form.is_admin.data
        EmployeeApiController.post_employee(first_name=firstname, last_name=lastname, salary=salary, position=position,
                                            is_admin=is_admin,
                                            email=email, password=password, department=department, birthday=birthday)
        send_password(email, password)
        flash(f"Register request for {form.firstname.data} {form.lastname.data} {form.department.data}")
        return redirect("index")
    return render_template("register_employee.html", form=form, title="Register Employee")


@app.route("/register_department", methods=["GET", "POST"])
@admins_only
@login_required
def register_department():
    form = RegisterDepartmentForm()
    if form.validate_on_submit():
        name = form.name.data
        DepartmentApiController.post_department(name=name)
        flash(f"Register request for {form.name.data}")
        return redirect("index")
    return render_template("register_department.html", form=form, title="Register Department")


@app.route("/department")
@app.route("/department/<uuid>")
@login_required
def department(uuid=None):
    statistics = {"employees": 0}
    if not uuid:
        departments = DepartmentApiController.get_all_departments()
        # if not departments:
        #     return abort(500)
    else:
        departments = [DepartmentApiController.get_department_by_uuid(uuid)]
        # if not departments[0]:
        #     return abort(404)
        statistics = StatisticApiController.get_department_statistics(uuid)
        # if not statistics:
        #     return abort(500)
    return render_template("department.html", title="Department", departments=departments, statistics=statistics)


@app.route("/employee")
@app.route("/employee/<uuid>")
@login_required
def employee(uuid=None):
    if not uuid:
        employees = EmployeeApiController.get_all_employees()
        # if not employees:
        #     return abort(500)
    else:
        employees = [EmployeeApiController.get_employee_by_uuid(uuid)]
        # if not employees[0]:
        #     return abort(404)
    return render_template("employee.html", title="Employee", employees=employees)


@app.route("/edit_employee/<uuid>", methods=['GET', "POST"])
@admins_only
@login_required
def admin_edit_employee(uuid):
    form = AdminEditProfileForm()
    employee = EmployeeApiController.get_employee_by_uuid(uuid)
    # if not employee:
    #     return abort(404)
    form.department.choices = [(dep["uuid"], dep["name"]) for dep in DepartmentApiController.get_all_departments()]
    fullname = employee["last_name"] + " " + employee["first_name"]
    if form.validate_on_submit():
        department = DepartmentApiController.get_department_by_uuid(form.department.data)
        EmployeeApiController.patch_employee(department=department, position=form.position.data,
                                             salary=form.salary.data, is_admin=form.is_admin.data, uuid=uuid)
        flash("Changes have been saved.")
        return redirect(url_for("admin_edit_employee", uuid=uuid))
    elif request.method == "GET":
        form.department.process_data(employee["department"]["uuid"])
        form.position.data = employee["position"]
        form.salary.data = employee["salary"]
        form.is_admin.process_data(employee["is_admin"])
    return render_template("admin_edit_employee.html", title="Edit Profile", form=form, fullname=fullname)


@app.route("/edit_employee", methods=['GET', "POST"])
@login_required
def edit_employee():
    form = EditProfileForm()
    if form.validate_on_submit():
        EmployeeApiController.patch_employee(first_name=form.firstname.data, last_name=form.lastname.data,
                                             birthday=form.birthday.data, email=form.email.data,
                                             password=form.password.data, uuid=current_user.uuid)
        flash("Changes have been saved.")
        return redirect(url_for("edit_employee"))
    elif request.method == "GET":
        form.firstname.data = current_user.first_name
        form.lastname.data = current_user.last_name
        form.email.data = current_user.email
        form.birthday.data = current_user.birthday
    return render_template("edit_employee.html", title="Edit Profile", form=form)


@app.route("/edit_department/<uuid>", methods=['GET', "POST"])
@admins_only
@login_required
def edit_department(uuid):
    form = EditDepartmentForm(uuid)
    department = DepartmentApiController.get_department_by_uuid(uuid)
    if form.validate_on_submit():
        DepartmentApiController.patch_department(name=form.name.data, uuid=uuid)
        flash("Changes have been saved.")
        return redirect(url_for("edit_department", uuid=uuid))
    elif request.method == "GET":
        form.name.data = department["name"]
    return render_template("edit_department.html", title="Edit Department", form=form)


@app.route("/delete_employee/<uuid>")
@admins_only
@login_required
def delete_employee(uuid):
    if current_user.is_admin:
        EmployeeApiController.delete_employee(uuid)
        flash(f"Employee deleted successfully")
    return redirect(url_for("employee"))


@app.route("/delete_department/<uuid>")
@admins_only
@login_required
def delete_department(uuid):
    if current_user.is_admin:
        DepartmentApiController.delete_department(uuid)
        flash(f"Department deleted successfully")
    return redirect(url_for("department"))


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="Page not found"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html', title="Unexpected error"), 500
