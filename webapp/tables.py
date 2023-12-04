from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func, select
from sqlalchemy.orm import column_property
from flask_login import current_user
from sqlalchemy import event, case

# Creates all Tables
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    week = db.Column(db.String(150), default=1)


class Workout(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.String(10), default = func.current_date())
    day = db.Column(db.String(12), nullable = False)
    week = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    workout_number = db.Column(db.Integer, nullable=False, unique=False)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150), nullable = False,)
    sets = db.Column(db.String(150))
    weight = db.Column(db.String(150))
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'))

class Routine(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    day = db.Column(db.String(12), nullable = False)
    exercise = db.Column(db.String(150), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Creates individual workout numbers for each User 
@event.listens_for(Workout, 'before_insert')
def update_workout_number(mapper, connection, target):
    max_workout_number = db.session.query(func.max(Workout.workout_number)).filter_by(user_id = current_user.id).scalar()
    if max_workout_number is None:
        target.workout_number = 1
    else:
        target.workout_number = max_workout_number + 1

# Orders the days in the Routine table
days_order = case(
    (Routine.day == 'Saturday', 1),
    (Routine.day == 'Sunday', 2),
    (Routine.day == 'Monday', 3),
    (Routine.day == 'Tuesday', 4),
    (Routine.day == 'Wednesday', 5),
    (Routine.day == 'Thursday', 6),
    (Routine.day == 'Friday', 7),
    else_=8
)
