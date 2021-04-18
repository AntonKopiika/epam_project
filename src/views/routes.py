import requests

from src import app
from flask import render_template


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Home")


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
