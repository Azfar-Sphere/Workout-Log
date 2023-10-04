from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func, select
from sqlalchemy.orm import column_property
from flask_login import current_user

# Creats user and workout tables
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime(timezone=True), default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    work =  column_property(
    select([func.coalesce(func.max(Workout.work), 0) + 1])
    .where(Workout.user_id == current_user.id)
    .correlate_except(Workout)
    .scalar_subquery()
)
# Makes it so that each user has their own work value that increments by 1 with each workout


