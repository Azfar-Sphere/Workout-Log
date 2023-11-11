from flask import Blueprint, render_template, send_from_directory, url_for
import os

pwa_bp = Blueprint("pwa", __name__)

# Sets routes for all
@pwa_bp.route('/<path:filename>')
def root_path(filename):
    directory = os.path.join(os.getcwd())
    return send_from_directory(directory, filename)

@pwa_bp.route('/webapp/<path:filename>')
def webapp_path(filename):
    directory = os.path.join(os.getcwd(), "webapp")
    return send_from_directory(directory, filename)

@pwa_bp.route('/webapp/templates/<path:filename>')
def templates_path(filename):
    directory = os.path.join(os.getcwd(), "webapp/templates")
    return send_from_directory(directory, filename)

@pwa_bp.route('/static/<path:filename>')
def static_path(filename):
    directory = os.path.join(os.getcwd(), "webapp/static")
    return send_from_directory(directory, filename)
