from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.column(db.Integer, primary_key=True)
    username = db.column(db.String(150), unique=True)
    password = db.column(db.String(150))
    