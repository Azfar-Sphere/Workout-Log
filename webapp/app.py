import os
from flask import Flask, render_template, session, redirect, request, url_for, flash
from flask_session import Session

from flask_sqlalchemy import SQLAlchemy
from pwa_routes import pwa_bp

app = Flask(__name__)
app.secret_key = "$2y$10$MQ72/iHjmp16XETNlq1E..BMlHrAGmMkHOxhu8MfO7.7toUb6fXdq"

# Registers Blueprints
app.register_blueprint(pwa_bp)

# Connects to users table
usersDb = SQLAlchemy()
DB_NAME = "users.db"

# Configures Flask to use Server-Side Session Storage
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
Session(app)

# Configures Database
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
usersDb.init_app(app)

# Defines index route
@app.route("/")
def index():
    render_template("index.html")
    

@app.route("/error")
def error(message):
    return render_template("error.html", error=message)    