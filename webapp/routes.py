from flask import render_template, Blueprint, request
from flask_login import login_required, current_user
from .tables import Workout
from . import db

routes = Blueprint("routes", __name__)

# Defines index route
@routes.route("/", methods=["GET", "POST"])
@login_required
def index():
    # Adds new workout
    if request.method == "POST":
        new_workout = Workout(user_id = current_user.id)
        db.session.add(new_workout)
        db.session.commit()

    workouts = db.session.query(Workout).filter(Workout.user_id == current_user.id).all()
    return render_template("index.html", workouts=workouts)

@routes.route("/error")
def error():
    return render_template("error.html")    