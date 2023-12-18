# Handles Authentication functionality
from . import db  
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .tables import User

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
        
        elif user:
            flash("Username taken", category='error')

        elif password != conpassword:
            flash("Passwords dont match", category='error')
        
        elif len(username) <= 4:
            flash("Please enter a username with 5 characters or more", category='error')

        elif len(password) <= 4:
            flash("Please enter a password with 5 characters or more", category='error')


        else:
            # Adds user detail to users database
            passwordHash = generate_password_hash(password)
            user = User(username=username, password=passwordHash)
            db.session.add(user)
            db.session.commit()

            login_user(user, remember=True)
            flash("Successfully registered", category="success")
            return redirect(url_for("routes.index"))
    
    return render_template("register.html")

# Defines Login Route
@auth.route("/login", methods=["GET", "POST"])
def login():
    # Receives username and password
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Checks login criteria
        user = User.query.filter_by(username=username).first()
        
        if not user is None:
            # If Login successful
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Logged in successfully", category='success')
                return redirect(url_for("routes.index"))
            else:
                flash('Incorrect Password', category='error')   
        else:
            flash("Incorrect username", category='error')

    return render_template("login.html")

#Logsout
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Successfully Logged Out", category='success')
    return redirect(url_for("auth.login"))

