from flask import Blueprint, render_template, send_from_directory, url_for
import os

pwa_bp = Blueprint("pwa", __name__)

# Sets PWA Config (Service-worker and manifest file)

# Intitaties Manifest Route
@pwa_bp.route("/manifest.json")
def manifest():
    directory = os.path.join(os.getcwd(), "webapp/manifest.json")
    return send_from_directory(directory, "manifest.json")

# Intiates service-worker route
@pwa_bp.route("/sw.js")
def service_worker():
    directory = os.path.join(os.getcwd(), "sw.js")
    return send_from_directory(directory, "sw.js")

# Intiates Main.Py 
@pwa_bp.route("/main.py")
def main():
    directory = os.path.join(os.getcwd(), "main.py")
    return send_from_directory(directory, "main.py")
