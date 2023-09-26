import os
from flask import Flask, render_template, session, redirect, request, url_for, flash
from flask_session import Session

from pwa_routes import pwa_bp

app = Flask(__name__)

# Registers Blueprints
app.register_blueprint(pwa_bp)

# Defines index route
@app.route("/")
def index():
    render_template("index.html")
    

@app.route("/error")
def error(message):
    return render_template("error.html", error=message)    