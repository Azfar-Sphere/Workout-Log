from flask import render_template, Blueprint, request, url_for, redirect, flash
from flask_login import login_required, current_user
from .tables import Workout, Exercise, Routine
from . import db
from sqlalchemy.sql import text

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
# id is Workout ID
def workout(id):
    user = db.session.query(Workout.user_id).filter_by(id = id).scalar()

    if user is None:
        return redirect(url_for("routes.error"))
    elif user != current_user.id:
        return redirect(url_for("routes.error"))

    workoutNumber = db.session.query(Workout.workout_number).filter_by(id = id).scalar();

    exercises = db.session.query(Exercise).filter_by(workout_id = id).all()
    return render_template("workout.html", workoutNumber = workoutNumber, exercises = exercises, user = user, workoutId = id)


@routes.route("/delete_w/<int:id>")
@login_required
#id is Workout ID
def deleteWorkout(id):
    workout = Workout.query.get(id)

    if workout is None:
        return redirect(url_for("routes.error"))
    elif workout.user_id != current_user.id:
        return redirect(url_for("routes.error"))
    
    workout_number_to_delete = workout.workout_number

    db.session.delete(workout)
    db.session.commit()

    workouts_to_update = Workout.query.filter(
    Workout.user_id == current_user.id,
    Workout.workout_number > workout_number_to_delete
    ).all()

    for workout in workouts_to_update:
        workout.workout_number -= 1;
    
    db.session.commit()

    return redirect(url_for("routes.index"))


@routes.route("/newexercise", methods=["POST"])
@login_required
def newExercise():
    # Checks for new excerise entry
    if request.method == "POST":
        exercise = request.form.get("e_name")
        exercise = exercise.capitalize()
        sets = request.form.get("sets")
        weight = request.form.get("weight")
        userId = request.form.get("user")
        workout_id = request.form.get("workoutId")

        #Checks if User is Valid user
        if int(userId) != current_user.id:
            return redirect(url_for("routes.error"))
        
        #Checks if user entered weight, otherwise default is bodyweight
        if not weight:
            weight = "Bodyweight"
        
        #Checks if exercise already exists previously in the workout, concatonates new sets and weight if it does
        if db.session.query(Exercise).filter_by(workout_id = workout_id, name = exercise).first():
            db.session.execute(
                text(
                    "UPDATE exercise SET sets = sets || ', ' || :sets, weight = weight || ', ' || :weight "
                    "WHERE workout_id = :workout_id AND name = :exercise"
                ),
                {"sets": sets, "weight": weight, "workout_id": workout_id, "exercise": exercise},
            )

        #Else adds new exercise
        else:
            new_exercise = Exercise(name = exercise, sets = sets, weight = weight, workout_id = workout_id)
            db.session.add(new_exercise)
        
        #Commits Changes
        db.session.commit()

    return redirect(url_for("routes.workout", id = workout_id))

@routes.route("/delete_e/<int:id>")
@login_required
#id is Exercise ID
def deleteExercise(id):
    workoutId = db.session.query(Exercise.workout_id).filter_by(id = id).scalar()
    user = db.session.query(Workout.user_id).filter_by(id = workoutId).scalar()

    if user is None:
        return redirect(url_for("routes.error"))
    elif user != current_user.id:
        return redirect(url_for("routes.error"))
    
    exercise = db.session.query(Exercise).filter_by(id = id).first()
    if exercise:
        db.session.delete(exercise)
        db.session.commit()

    return redirect(url_for("routes.workout", id = workoutId))

@routes.route("/routine", methods=["POST", "GET"])
@login_required
def routine():
    
    if request.method == "POST":
        day = request.form.get("day")
        exercise = request.form.get("exercise")
        exercise = exercise.capitalize()

        if db.session.query(Routine).filter_by(day = day, exercise = exercise, user_id = current_user.id):
            flash("Exercise Already Exists For this Day!", category='error')

        else:
            new_exercise = Routine(day = day, exercise = exercise, user_id = current_user.id)
            db.session.add(new_exercise)
            db.session.commit()

    return render_template("routine.html")