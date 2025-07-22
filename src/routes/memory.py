from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from ..services import MemoryManagement

memory_bp = Blueprint('memory', __name__, url_prefix='/memory')

@memory_bp.route('/', methods=["GET", "POST"])
def upload():
    if not session.get("user_id", False):
        flash("Please login first", "warning")
        return redirect(url_for("user.login"))

    if not session.get("vault_info", False):
        return redirect(url_for("settings.index"))

    if request.method == "GET":
        return render_template('memory_upload.html', title="Homepage", user=session["user_html_package"], vault=session["vault_info"])
    if request.method == "POST":

        MemoryManagement.upload_memory(description=request.form["description"],
                                       date=request.form["date"],
                                       latitude=request.form.get("latitude", None),
                                       longitude=request.form.get("longitude", None),
                                       image_file=request.files.get("image"),
                                       vault_id=session.get("vault_info")["vault_id"])

        return render_template('memory_upload.html', title="Homepage", user=session["user_html_package"], vault=session["vault_info"])