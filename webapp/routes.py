from flask import render_template, Blueprint, request, url_for, redirect, flash
from flask_login import login_required, current_user
from .tables import Workout, Exercise, Routine, days_order
from . import db
from sqlalchemy.sql import text, case

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

    days = db.session.query(Routine.day).filter_by(user_id = current_user.id).distinct().order_by(days_order).all()
    days = [day[0] for day in days]

    workouts = db.session.query(Workout).filter_by(user_id = current_user.id).all()

    return render_template("index.html", days = days, workouts = workouts)

@routes.route("/dayworkout", methods=["POST", "GET"])
@login_required
def newWorkout():
    day = request.form.get("day")

    if request.method == "POST":

        if db.session.query(Workout).filter_by(day = day, user_id = current_user.id).scalar() is not None:
            id = db.session.query(Workout.id).filter_by(day = day, user_id = current_user.id).first()
            id = int(id[0]) if id is not None else None 

            return redirect(url_for("routes.workout", id = id))

        new_workout = Workout(day = day, user_id = current_user.id)
        db.session.add(new_workout)
        db.session.commit()

    id = db.session.query(Workout.id).filter_by(day = day, user_id = current_user.id).first()
    id = int(id[0]) if id is not None else None

    return redirect(url_for("routes.workout", id = id))

#Defines Each Workout Route
@routes.route("/workout/<int:id>")
@login_required
# id is Workout ID
def workout(id):
    workout_id = id
    user = db.session.query(Workout.user_id).filter_by(id = workout_id).scalar()

    if user is None:
        return redirect(url_for("routes.error"))
    elif user != current_user.id:
        return redirect(url_for("routes.error"))

    workout_day = db.session.query(Workout.day).filter_by(id = workout_id).scalar()
    exercises = db.session.query(Routine.exercise).filter_by(day = workout_day, user_id = current_user.id).all()
    exercises = [exercise[0] for exercise in exercises]

    for exercise in exercises:
        if db.session.query(Exercise).filter_by(name = exercise, workout_id = workout_id).scalar() is None:
            new_exercise = Exercise(name = exercise, workout_id = workout_id)
            db.session.add(new_exercise)

    db.session.commit()

    exercises = db.session.query(Exercise).filter_by(workout_id = workout_id).all()

    return render_template("workout.html", workout_day = workout_day, exercises = exercises, user = user, workoutId = workout_id)

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


@routes.route("/addsets", methods=["POST"])
@login_required
def addSets():
    # Checks for new excerise entry
    if request.method == "POST":
        exercise = request.form.get("e_name")
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
        if db.session.query(Exercise.sets).filter_by(workout_id = workout_id, name = exercise).scalar() is not None:
            db.session.execute(
                text(
                    "UPDATE exercise SET sets = sets || ', ' || :sets, weight = weight || ', ' || :weight "
                    "WHERE workout_id = :workout_id AND name = :exercise"
                ),
                {"sets": sets, "weight": weight, "workout_id": workout_id, "exercise": exercise},
            )

        #Else adds new exercise
        else:
            db.session.execute(
                text(
                    "UPDATE exercise SET sets = :sets, weight = :weight "
                    "WHERE workout_id = :workout_id and name =:exercise"
                ),
                {"sets": sets, "weight": weight, "workout_id": workout_id, "exercise": exercise},
            )
        
        #Commits Changes
        db.session.commit()

    return redirect(url_for("routes.workout", id = workout_id))

@routes.route("/delete_e/<string:day>/<string:exercise>")
@login_required
#id is Exercise ID
def deleteExercise(day, exercise):
    exercise_to_delete = db.session.query(Routine).filter_by(day = day, exercise = exercise, user_id = current_user.id).first()

    if exercise_to_delete:
        db.session.delete(exercise_to_delete)
        db.session.commit()

    else:
        flash("Error Deleting Exercise", category='error')

    return redirect(url_for("routes.routine"))

@routes.route("/routine", methods=["POST", "GET"])
@login_required
def routine():

    if request.method == "POST":
        day = request.form.get("day")
        day = day.capitalize()
        exercise = request.form.get("exercise")
        exercise = exercise.title()

        if not exercise:
            flash("Please Enter Exercise!", category='error')
        
        elif db.session.query(Routine).filter_by(day = day, exercise = exercise, user_id = current_user.id).first():
            flash("Exercise Already Exists For this Day!", category='error')

        else:
            new_exercise = Routine(day = day, exercise = exercise, user_id = current_user.id)
            db.session.add(new_exercise)
            db.session.commit()

    days = db.session.query(Routine.day).filter_by(user_id = current_user.id).distinct().order_by(days_order).all()
    days = [day[0] for day in days]

    exercises = db.session.query(Routine).filter_by(user_id = current_user.id).all()

    return render_template("routine.html", days = days, exercises = exercises)

@routes.route("/archive")
@login_required
def archive():
    workouts = db.session.query(Workout).filter_by(user_id = current_user.id).all()
    
    return render_template("archive.html", workouts = workouts)



#Defines Error Route
@routes.route("/error")
def error():
    return render_template("error.html")    
