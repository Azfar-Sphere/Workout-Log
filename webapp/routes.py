from flask import render_template, Blueprint, request, url_for, redirect, flash
from flask_login import login_required, current_user
from .tables import User, Workout, Exercise, Routine, days_order
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

    # Gets The Days From Routine
    days = db.session.query(Routine.day).filter_by(user_id = current_user.id).distinct().order_by(days_order).all()
    days = [day[0] for day in days]

    # Gets all the workouts for the user
    workouts = db.session.query(Workout).filter_by(user_id = current_user.id).all()

    # Gets the current weeks for the user
    week = db.session.query(User.week).filter_by(id = current_user.id).first()
    week = week[0]

    return render_template("index.html", days = days, workouts = workouts, week=week)

# Defines the route when a new workout for a day is created
@routes.route("/dayworkout", methods=["POST", "GET"])
@login_required
def newWorkout():
    # Gets day and week from the form
    day = request.form.get("day")
    week = request.form.get("week")

    if request.method == "POST":

        # Checks if workout exists already
        workout = db.session.query(Workout).filter_by(day = day, week = week, user_id = current_user.id).first()

        # Case if it does exist, redirects
        if workout is not None:
            id = workout.id
            return redirect(url_for("routes.workout", id = id))

        # Creates new workout if workout does not exist
        new_workout = Workout(day = day, week = week, user_id = current_user.id)
        db.session.add(new_workout)
        db.session.commit()

    # Gets the workout id and redirects
    id = db.session.query(Workout.id).filter_by(day = day, week = week, user_id = current_user.id).first()
    id = int(id[0]) if id is not None else None
 
    return redirect(url_for("routes.workout", id = id))

#Defines Each Workout Route
@routes.route("/workout/<int:id>")
@login_required
# id variable is Workout ID
def workout(id):
    workout_id = id
    # Gets the user
    user = db.session.query(Workout.user_id).filter_by(id = workout_id).scalar()

    # Validates User
    if user is None:
        return redirect(url_for("routes.error"))
    elif user != current_user.id:
        return redirect(url_for("routes.error"))

    # Gets the workout day
    workout_day = db.session.query(Workout.day).filter_by(id = workout_id).scalar()

    # Retrieves exercises for that day
    exercises = db.session.query(Routine.exercise).filter_by(day = workout_day, user_id = current_user.id).all()
    exercises = [exercise[0] for exercise in exercises]

    # Assigns exercise to the workout if they aren't previously assigned
    for exercise in exercises:
        if db.session.query(Exercise).filter_by(name = exercise, workout_id = workout_id).scalar() is None:
            new_exercise = Exercise(name = exercise, workout_id = workout_id)
            db.session.add(new_exercise)

    db.session.commit()

    # Retrieves all the exercises for that workout
    exercises = db.session.query(Exercise).filter_by(workout_id = workout_id).all()

    return render_template("workout.html", workout_day = workout_day, exercises = exercises, user = user, workoutId = workout_id)

#Defines the route Delete a workout
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

    return redirect(url_for("routes.archive"))

# Defines route to add sets and weight to the exercise
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

# Defines route to delete sets
@routes.route("/deletesets", methods=["GET", "POST"])
@login_required
def deleteSets():
    # Gets Exercise ID
    e_id = request.form.get("e_id")

    if request.method == "POST":

        # Retreives the exercise from the table to be updated
        exercise_to_update = db.session.query(Exercise).filter_by(id = e_id).first()

        # Checks if exercise exists
        if exercise_to_update:
            exercise_to_update.sets = None
            exercise_to_update.weight = None
            db.session.commit()
            
            flash("Sets Successfully Deleted", category="success")

        else:
            flash("Error deleting exercise", category="error")

    # Redirects to workout page by getting id first
    workout_id = db.session.query(Exercise.workout_id).filter_by(id = e_id).first()
    workout_id = workout_id[0]

    return redirect(url_for("routes.workout", id = workout_id))

# Defines route to delete exercise in a particular routine
@routes.route("/delete_e/<string:day>/<string:exercise>")
@login_required
def deleteExercise(day, exercise):
    # Retreives the exercise to delete
    exercise_to_delete = db.session.query(Routine).filter_by(day = day, exercise = exercise, user_id = current_user.id).first()

    # If exercise exists, then deletes
    if exercise_to_delete:
        db.session.delete(exercise_to_delete)
        db.session.commit()

    else:
        flash("Error Deleting Exercise", category='error')

    return redirect(url_for("routes.routine"))

# Defines routine route
@routes.route("/routine", methods=["POST", "GET"])
@login_required
def routine():

    # In order to add more days and exercies, a POST request is made
    if request.method == "POST":
        # Retrieves days and the exercise, formats appropriately
        day = request.form.get("day")
        day = day.capitalize()
        exercise = request.form.get("exercise")
        exercise = exercise.title()

        # If no exercise is entered
        if not exercise:
            flash("Please Enter Exercise!", category='error')
        
        # If the same exercise for the same day is entered
        elif db.session.query(Routine).filter_by(day = day, exercise = exercise, user_id = current_user.id).first():
            flash("Exercise Already Exists For this Day!", category='error')

        # Adds new exercise
        else:
            new_exercise = Routine(day = day, exercise = exercise, user_id = current_user.id)
            db.session.add(new_exercise)
            db.session.commit()

    # Gets all the days the user worksout
    days = db.session.query(Routine.day).filter_by(user_id = current_user.id).distinct().order_by(days_order).all()
    days = [day[0] for day in days]

    # Gets all the exercises for the user
    exercises = db.session.query(Routine).filter_by(user_id = current_user.id).all()

    return render_template("routine.html", days = days, exercises = exercises)

# Defines archive route
@routes.route("/archive")
@login_required
def archive():
    # Gets workouts and the total weeks the user has been exercising for
    workouts = db.session.query(Workout).filter_by(user_id = current_user.id).all()
    weeks = db.session.query(Workout.week).filter_by(user_id = current_user.id).distinct().all()
    weeks = [week[0] for week in weeks]

    return render_template("archive.html", workouts = workouts, weeks = weeks)  

# Defines route to change to next week
@routes.route("/incrementweek", methods=["POST", "GET"])
@login_required
def increment_week():
    if request.method == "POST":    
        # Updates 'week' column in the User table 
        user = db.session.query(User).filter_by(id = current_user.id).first()
        new_week = int(user.week) + 1;

        user.week = new_week
        db.session.commit()

    return redirect(url_for("routes.index"))

# Defines Compare route
@routes.route("/compare", methods=["POST", "GET"])
@login_required
def compare():
    days = db.session.query(Routine.day).filter_by(user_id = current_user.id).distinct().order_by(days_order).all()
    days = [day[0] for day in days]

    if request.method == "POST":
        week_a = request.form.get("week_a")
        week_b = request.form.get("week_b")
        exercise = request.form.get("exercise")
        day = request.form.get("day") 

        week_a_id = db.session.query(Workout).filter_by(user_id = current_user.id, week = week_a, day = day).first()
        week_a_id = week_a_id.id
        week_b_id = db.session.query(Workout).filter_by(user_id = current_user.id, week = week_b, day = day).first()
        week_b_id = week_b_id.id

        exercise_a = db.session.query(Exercise).filter_by(workout_id = week_a_id, name = exercise).first()
        exercise_b = db.session.query(Exercise).filter_by(workout_id = week_b_id, name = exercise).first()

        return render_template("compare.html", days = days, exercise_a = exercise_a ,exercise_b = exercise_b, week_a = week_a, week_b = week_b)


    return render_template("compare.html", days = days, exercise_a = 0, exercise_b = 0, week_a = 0, week_b = 0)

#Defines Error Route
@routes.route("/error")
def error():
    return render_template("error.html")    
