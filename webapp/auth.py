# Handles Authentication functionality
from app import app, db  
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from tables import User

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["GET", "POST"])
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
            return redirect(url_for("app.index"))
    
    return render_template("register.html")

# Defines Login Route
@auth.route("/login", methods=["GET", "POST"])
def login():
    # Receives username and password
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user is None:
            flash("Incorrect username", category='error')

        elif not check_password_hash(user.password, password):
            flash("Incorrect Password", category='error')

        # If Login successful
        login_user(user, remember=True)
        flash("Logged in successfully", category='success')
        return redirect(url_for("app.index"))

    return render_template("login.html")

#Logsout
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

