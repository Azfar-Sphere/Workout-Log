from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Creats user and workout tables
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    work =  db.Column(db.Integer, nullable=False, default=lambda: Workout.query.count() + 1)
    date = db.Column(db.DateTime(timezone=True), default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))