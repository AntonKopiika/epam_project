from src import app
from flask import render_template


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="Page not found")


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html', title="Unexpected error")
