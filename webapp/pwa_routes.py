from flask import Blueprint, render_template, send_from_directory, url_for

pwa_bp = Blueprint("pwa", __name__)

# Sets PWA Config (Service-worker and manifest file)

# Intitaties Manifest Route
@pwa_bp.route("/manifest.json")
def manifest():
    return send_from_directory("/home/azfar/Workout-Log/webapp/", "manifest.json")

# Intiates service-worker route
@pwa_bp.route("/sw.js")
def service_worker():
    return send_from_directory("/home/azfar/Workout-Log", "sw.js")
# Intiates service-worker files

@pwa_bp.route("/static/logos/manifest-icon-192.maskable.png")
def icon192():
    return url_for("static", filename="manifest-icon-192.maskable.png")

@pwa_bp.route("/static/logos/manifest-icon-512.maskable.png")
def icon512():
    return url_for("static", filename="manifest-icon-512.maskable.png")


