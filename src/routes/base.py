from flask import Blueprint, redirect, url_for

base_bp = Blueprint('base', __name__, url_prefix='/')

@base_bp.route('/')
def index():
    return redirect(url_for("memory.index"))