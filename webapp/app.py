from flask import Flask, render_template, send_from_directory, session, redirect, request, url_for, flash
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connects to users table
usersDb = SQLAlchemy()
DB_NAME = "users.db"

# Configures Flask to use Server-Side Session Storage
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
# Configures Database
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
Session(app)

# Sets PWA Config (Service-worker and manifest file)
#####################################################################
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
# Sends Icon route
@app.route("/templates/static/icon.png")
def icon():
    return send_from_directory("/home/azfar/Workout-Log/webapp/templates/static", "icon.png")
# Renders offline.html if there is no internet
@app.route("/offline.html")
def offline():
    return render_template("offline.html")
#####################################################################

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
        usersCursor.execute("SELECT username FROM users ")
        usernameRow = usersCursor.fetchall()

        # Checks valid username and password
        if not username or not password:
            return render_template("error.html", error="Invalid Username/Password")

        elif username in usernameRow:
            return render_template("error.html", error="Username not available")

        elif password != conpassword:
            return render_template("error.html", error="Passwords do not match!")

        else:
            # Adds user detail to users database
            passwordHash = generate_password_hash("password")
            usersCursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, passwordHash))
            connUsers.commit()
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

        usersCursor.execute("SELECT username, hash FROM users WHERE username = ?", (username,))
        usernameRow = usersCursor.fetchone()

        # Checks validity of login details
        if not usernameRow:
            return render_template("error.html", error="Invalid Username")

        if not check_password_hash(usernameRow[1], "password"):
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