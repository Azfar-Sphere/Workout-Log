from flask import Blueprint, render_template, send_from_directory, url_for
import os

pwa_bp = Blueprint("pwa", __name__)

# Sets routes for all possible paths
@pwa_bp.route("/<filename>")
def root_path(filename):
    directory = os.path.join(os.getcwd())
    return send_from_directory(directory, filename)

@pwa_bp.route("/webapp/<filename>")
def webapp_path(filename):
    directory = os.path.join(os.getcwd(), "webapp")
    return send_from_directory(directory, filename)

@pwa_bp.route("/webapp/templates/<filename>")
def templates_path(filename):
    directory = os.path.join(os.getcwd(), "webapp/templates")
    return send_from_directory(directory, filename)

@pwa_bp.route("/webapp/templates/static/<filename>")
def static_path(filename):
    directory = os.path.join(os.getcwd(), "webapp/templates/static")
    return send_from_directory(directory, filename)

@pwa_bp.route("/webapp/__pycache__/<filename>")
def pycache_path(filename):
    directory = os.path.join(os.getcwd(), "webapp/__pycache__")
    return send_from_directory(directory, filename)

