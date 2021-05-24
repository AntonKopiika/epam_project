"""
This module implements rendering home and about pages
"""
from functools import wraps
from src import app
from flask import render_template, flash, redirect, url_for
from flask_login import current_user


def admins_only(func):
    """
    wrapper for giving permission to admins only pages
    :param func: rendering function
    :return: function if access is permitted
    """
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
    """
    method for rendering home page
    :return: home page view
    """
    return render_template("index.html", title="Home")
