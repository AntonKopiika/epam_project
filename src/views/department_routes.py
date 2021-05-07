from src import app
from flask import render_template, flash, redirect, url_for, request
from src.forms.departments.register_department import RegisterDepartmentForm
from src.forms.departments.edit_department import EditDepartmentForm
from flask_login import current_user, login_required
from src.rest.api_controllers import DepartmentApiController, StatisticApiController
from src.views.base_routes import admins_only


@app.route("/register_department", methods=["GET", "POST"])
@admins_only
@login_required
def register_department():
    form = RegisterDepartmentForm()
    if form.validate_on_submit():
        name = form.name.data
        response = DepartmentApiController.post_department(name=name)
        if response.status_code == 201:
            flash(f"{form.name.data} successfully registered")
        else:
            flash(f"Something went wrong while creating department")
        return redirect(url_for("department"))
    return render_template("register_department.html", form=form, title="Register Department")


@app.route("/department")
@app.route("/department/<uuid>")
@login_required
def department(uuid=None):
    if not uuid:
        departments = DepartmentApiController.get_all_departments()
        statistics = {"employees": 0}
    else:
        departments = [DepartmentApiController.get_department_by_uuid(uuid)]
        statistics = StatisticApiController.get_department_statistics(uuid)
    return render_template("department.html", title="Department", departments=departments, statistics=statistics)


@app.route("/edit_department/<uuid>", methods=['GET', "POST"])
@admins_only
@login_required
def edit_department(uuid):
    form = EditDepartmentForm(uuid)
    department = DepartmentApiController.get_department_by_uuid(uuid)
    if form.validate_on_submit():
        response = DepartmentApiController.patch_department(name=form.name.data, uuid=uuid)
        if response.status_code == 200:
            flash("Changes have been saved")
        else:
            flash(f"Something went wrong while editing")
        return redirect(url_for("edit_department", uuid=uuid))
    elif request.method == "GET":
        form.name.data = department["name"]
    return render_template("edit_department.html", title="Edit Department", form=form)


@app.route("/delete_department/<uuid>")
@admins_only
@login_required
def delete_department(uuid):
    if current_user.is_admin:
        response = DepartmentApiController.delete_department(uuid)
        if response.status_code == 204:
            flash(f"Department deleted successfully")
        else:
            flash(f"Something went wrong while deleting")
    return redirect(url_for("department"))
