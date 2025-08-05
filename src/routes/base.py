"""
Base module for HTTP routes.
Defines base blueprint and logic for handeling requests to root URL.
Redirects requests based on login status.
"""
from flask import Blueprint, redirect, url_for, session

base_bp = Blueprint('base', __name__, url_prefix='/')


@base_bp.route('/', methods=["GET"])
def index():
    """
    Handles GET requests to root URL.

    Redirects authenticated users to memory upload.
    Redirects unauthenticated users to login page.

    Returns:
        Reponse: A redirect to appropriate route.
    """
    if session.get("user_id", False):
        return redirect(url_for("memory.upload"))

    return redirect(url_for("user.login"))
