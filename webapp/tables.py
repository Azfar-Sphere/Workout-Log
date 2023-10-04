from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func, select
from sqlalchemy.orm import column_property
from flask_login import current_user
from sqlalchemy import event

# Creats user and workout tables
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
class Workout(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime(timezone=True), default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    workout_number = db.Column(db.Integer, nullable=False, unique=False)

# Creates individual workout numbers for each User 
@event.listens_for(Workout, 'before_insert')
def update_workout_number(mapper, connection, target):
    max_workout_number = db.session.query(func.max(Workout.workout_number)).filter_by(user_id = current_user.id).scalar()
    if max_workout_number is None:
        target.workout_number = 1
    else:
        target.workout_number = max_workout_number + 1
