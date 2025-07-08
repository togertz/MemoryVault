from flask import Blueprint, render_template, redirect, url_for

base_bp = Blueprint('base', __name__, url_prefix='/')

@base_bp.route('/')
def index():
    return render_template('base.html', title="Homepage", placeholder="Homepage")