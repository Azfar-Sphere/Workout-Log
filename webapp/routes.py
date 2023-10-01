from flask import render_template, Blueprint
from flask_login import login_required

routes = Blueprint("routes", __name__)

# Defines index route
@routes.route("/")
@login_required
def index():
    return render_template("index.html")

@routes.route("/error")
def error():
    return render_template("error.html")    