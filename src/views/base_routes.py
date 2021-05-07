from functools import wraps
from src import app
from flask import render_template, flash, redirect, url_for
from flask_login import current_user


def admins_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_admin:
            return func(*args, **kwargs)
        flash(f"Access denied")
        return redirect(url_for("index"))

    return wrapper


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Home")


@app.route("/about")
def about():
    return render_template("about.html", title="About")
