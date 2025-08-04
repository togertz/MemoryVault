from flask import Blueprint, redirect, url_for, session

base_bp = Blueprint('base', __name__, url_prefix='/')


@base_bp.route('/')
def index():
    if session.get("user_id", False):
        return redirect(url_for("memory.upload"))

    return redirect(url_for("user.login"))
