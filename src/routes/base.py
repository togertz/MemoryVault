from flask import Blueprint, render_template, redirect, url_for, session
from ..services import UserManagement

base_bp = Blueprint('base', __name__, url_prefix='/')

@base_bp.route('/')
def index():
    if session.get("user_id", False):
        return redirect(url_for("memory.upload"))
    else:
        return redirect(url_for("user.login"))