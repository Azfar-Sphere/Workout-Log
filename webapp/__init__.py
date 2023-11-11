import os
from flask import Flask, render_template, send_from_directory, session, redirect, request, url_for, flash
from flask_session import Session
from flask_login import LoginManager, login_required, current_user
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()
DB_NAME = "data.db"

def create_app():
    # Creates App with Static Files Directory
    app = Flask(__name__, static_url_path="/webapp/templates/static")
    app.secret_key = "$2y$10$MQ72/iHjmp16XETNlq1E..BMlHrAGmMkHOxhu8MfO7.7toUb6fXdq"

    # Registers Blueprints
    from .pwa_routes import pwa_bp
    from .auth import auth
    from .routes import routes
    
    app.register_blueprint(pwa_bp)
    app.register_blueprint(auth)
    app.register_blueprint(routes)

    # Configures Database
    from .tables import User

    db_path = os.path.join(app.root_path, DB_NAME)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    db.init_app(app)
    # Creates Database
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
            print("Created Database")
    else:
        print("Database exists, skipping database creation")

    # Configures Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app


