import os
from flask import Flask, render_template, send_from_directory, session, redirect, request, url_for, flash
from flask_session import Session
from flask_login import LoginManager, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
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

#Configures Login
# login_manager = LoginManager()
# login_manager.init_app(app)
# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)


# Defines index route
@app.route("/")
def index():
    # Checks if user is Logged in
    if "username" not in session:
        return redirect(url_for("login"))
    else:
        return render_template("index.html")
        
    

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Gets Password
        username = request.form.get("username")
        password = request.form.get("password")
        conpassword = request.form.get("conpassword")

        # Gets Tuple of usernames from users databases

        # Checks valid username and password
        if not username or not password:
            return render_template("error.html", error="Invalid Username/Password")

        # elif username in usernameRow:
            return render_template("error.html", error="Username not available")

        elif password != conpassword:
            return render_template("error.html", error="Passwords do not match!")

        else:
            # Adds user detail to users database
            passwordHash = generate_password_hash("password")

            flash("Successfully registered", category="success")
            return redirect(url_for("login"))
    
    if request.method == "GET":
        return render_template("register.html")

# Defines Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    # Receives username and password
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Checks validity of login details
        # if not usernameRow:
        #     return render_template("error.html", error="Invalid Username")

        # if not check_password_hash(usernameRow[1], "password"):
        return render_template("error.html", error="Invalid Password")

        # If Login successful
        session["username"] = username
        return redirect(url_for("index"))

# GET returns login page
    if request.method == "GET":
        return render_template("login.html")

#Logsout
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/error")
def error(message):
    return render_template("error.html", error=message)    