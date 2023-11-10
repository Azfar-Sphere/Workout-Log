from flask import Blueprint, render_template, send_from_directory

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

# Intiates CSS and JS for the HTML page
@pwa_bp.route("/static/styles.css")
def css():
    return send_from_directory("/home/azfar/Workout-Log/webapp/templates/static", "styles.css")
# Intiates app.js route
@pwa_bp.route("/static/app.js")
def app_js():
    return send_from_directory("/home/azfar/Workout-Log/webapp/templates/static", "app.js")
# Intiates workout.js route
@pwa_bp.route("/static/workout.js")
def workout_js():
    return send_from_directory("/home/azfar/Workout-Log/webapp/templates/static", "workout.js")
# Sends Icon route
@pwa_bp.route("/templates/static/icon.png")
def icon():
    return send_from_directory("/home/azfar/Workout-Log/webapp/templates/static", "icon.png")

@pwa_bp.route("/templates/static/logos/manifest-icon-192.maskable.png")
def icon192():
    return send_from_directory("/home/azfar/Workout-Log/webapp/templates/static/logos", "manifest-icon-192.maskable.png")

@pwa_bp.route("/templates/static/logos/manifest-icon-512.maskable.png")
def icon512():
    return send_from_directory("/home/azfar/Workout-Log/webapp/templates/static/logos", "manifest-icon-512.maskable.png")
# Renders offline.html if there is no internet for service-worker
@pwa_bp.route("/offline.html")
def offline():
    return render_template("offline.html")

