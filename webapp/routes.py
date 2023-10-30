from flask import render_template, Blueprint, request, url_for, redirect
from flask_login import login_required, current_user
from .tables import Workout, Exercise
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

    workouts = db.session.query(Workout).filter_by(user_id = current_user.id).order_by(Workout.date).all()
    return render_template("index.html", workouts=workouts)

#Defines Error Route
@routes.route("/error")
def error():
    return render_template("error.html")    

#Defines Each Workout Route
@routes.route("/workout/<int:id>")
@login_required
def workout(id):
    user = db.session.query(Workout.user_id).filter_by(id = id).scalar()

    if user is None:
        return redirect(url_for("routes.error"))
    elif user != current_user.id:
        return redirect(url_for("routes.error"))

    workoutNumber = db.session.query(Workout.workout_number).filter_by(id = id).scalar();

    exercises = db.session.query(Exercise).filter_by(workout_id = id).all()
    return render_template("workout.html", workoutNumber = workoutNumber, exercises = exercises)