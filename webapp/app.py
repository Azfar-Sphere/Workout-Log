from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# First two routes set-up PWA configuration
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

@app.route("/templates/static/app.js")
def app_js():
    return send_from_directory("/home/azfar/Workout-Log/webapp/templates/static", "app.js")

# Defines index route
@app.route("/")
def hello():
    return render_template("layout.html")