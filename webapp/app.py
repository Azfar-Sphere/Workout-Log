from flask import Flask, render_template, send_from_directory, session, redirect, request, url_for
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

# Connects to users table
connUsers = sqlite3.connect("users.db")
usersCursor = connUsers.cursor()

# Configures Flask to use Server-Side Session Storage
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
Session(app)

#####################################################################
# Sets PWA Config
# Intitaties Manifest Route
@app.route("/manifest.json")
def manifest():
    return send_from_directory("/home/azfar/Workout-Log/webapp/", "manifest.json")

# Intiates service-worker route
@app.route("/service-worker.js")
def service_worker():
    return send_from_directory("/home/azfar/Workout-Log/webapp/", "service-worker.js")

# Intiates CSS and JS for the HTML page
@app.route("/templates/static/styles.css")
def css():
    return send_from_directory("/home/azfar/Workout-Log/webapp/templates/static", "styles.css")
# Intiates app.js route
@app.route("/templates/static/app.js")
def app_js():
    return send_from_directory("/home/azfar/Workout-Log/webapp/templates/static", "app.js")

#####################################################################

# Defines index route
@app.route("/")
def index():
    # Checks if user is Logged in
    if "username" in session:
        return render_template("index.html")
    else:
        return redirect(url_for("login"))
    

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Gets Password
        username = request.form["username"]
        password = request.form["password"]
        conpassword = request.form["conpassword"]

        # Gets Tuple of usernames from users databases
        usersCursor.execute("SELECT username FROM users ")
        usernameRow = usersCursor.fetchall()

        # Checks valid username and password
        if not username or not password:
            error("Please Enter Username and Password")

        if username in usernameRow:
            error("Username Taken")

        if password != conpassword:
            error("Password do not match!")    

        # Adds user detail to users database
        passwordHash = generate_password_hash("password")
        usersCursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, passwordHash))
        redirect(url_for("login"))
    
    return render_template("register.html")

# Defines Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    # Receives username and password
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        usersCursor.execute("SELECT username, hash FROM users WHERE username = ?", (username,))
        usernameRow = usersCursor.fetchone()

        # Checks validity of login details
        if not usernameRow:
            error("Invalid username")

        if not check_password_hash(usernameRow[1], "password"):
            error("Incorrect Password")

        # If Login successful
        session["username"] = username
        return redirect(url_for("index"))

# GET returns login page
    return render_template("login.html")

#Logsout
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/error")
def error(message):
    return render_template("error.html", error=message)    