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
    return render_template("workout.html", workoutNumber = workoutNumber, exercises = exercises, user = user, workoutId = id)

@routes.route("/newworkout", methods=["POST"])
@login_required
def newWorkout():
    if request.method == "POST":
        exercise = request.form.get("e_name")
        sets = request.form.get("sets")
        weight = request.form.get("weight")
        userId = request.form.get("user")
        workoutId = request.form.get("workoutId")

        if int(userId) != current_user.id:
            return redirect(url_for("routes.error"))
        
        new_exercise = Exercise(name = exercise, sets = sets, weight = weight, workout_id = workoutId)
        db.session.add(new_exercise)
        db.session.commit()

    return redirect(url_for("routes.index"))


