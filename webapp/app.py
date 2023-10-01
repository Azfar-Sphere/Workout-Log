import os
from flask import Flask, render_template, send_from_directory, session, redirect, request, url_for, flash
from flask_session import Session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from pwa_routes import pwa_bp
from tables import User

app = Flask(__name__)
app.secret_key = "$2y$10$MQ72/iHjmp16XETNlq1E..BMlHrAGmMkHOxhu8MfO7.7toUb6fXdq"

# Registers Blueprints
app.register_blueprint(pwa_bp)

# Connects to users table
db = SQLAlchemy()
DB_NAME = "users.db"

# Configures Flask to use Server-Side Session Storage
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
Session(app)

# Configures Database
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
db.init_app(app)

#Configures Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# Defines index route
@app.route("/")
@login_required
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

        # Gets username for database
        user = User.query.filter_by(username=username).first()
        # Checks valid username and password
        if not username or not password:
            flash("Please enter username and password", category='error')

        elif username in user:
            flash("Username taken", category='error')

        elif password != conpassword:
            flash("Passwords dont match", category='error')

        else:
            # Adds user detail to users database
            passwordHash = generate_password_hash("password")
            new_user = User(username=username, password=passwordHash)
            db.session.add(new_user)
            db.session.commit()

            login_user(user)
            flash("Successfully registered", category="success")
            return redirect(url_for("index"))
    
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
@login_required
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/error")
def error(message):
    return render_template("error.html", error=message)    