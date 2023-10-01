import os
from flask import Flask, render_template, send_from_directory, session, redirect, request, url_for, flash
from flask_session import Session
from flask_login import LoginManager, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from pwa_routes import pwa_bp
from auth import auth
from auth import configure_login

app = Flask(__name__)
app.secret_key = "$2y$10$MQ72/iHjmp16XETNlq1E..BMlHrAGmMkHOxhu8MfO7.7toUb6fXdq"

if __name__ == "__app__":
    app.run(debug=True)

# Registers Blueprints
app.register_blueprint(pwa_bp)
app.register_blueprint(auth)

# Connects to users table
db = SQLAlchemy()
DB_NAME = "users.db"

# Configures Database
db_path = os.path.join(app.root_path, DB_NAME)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
db.init_app(app)
# Creates Database
if not os.path.exists(db_path):
    with app.app_context():
        db.create_all
        print("Created Database")
else:
    print("Database exists, skipping database creation")

# Configures Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# Defines index route
@auth.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/error")
def error():
    return render_template("error.html")    