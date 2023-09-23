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


# Defines index route
@app.route("/")
def hello():
    return render_template("layout.html")