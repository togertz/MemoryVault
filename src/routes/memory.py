from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from ..services import MemoryManagement

memory_bp = Blueprint('memory', __name__, url_prefix='/memory')


@memory_bp.route('/', methods=["GET", "POST"])
def upload():
    if not session.get("user_id", False):
        flash("Please login first", "warning")
        return redirect(url_for("user.login"))

    if not session.get("vault_info", False) and not session.get("family_vault_info", False):
        return redirect(url_for("settings.index"))

    if request.method == "GET":
        return render_template('memory_upload.html',
                               title="Homepage",
                               user=session["user_info"],
                               vault=session.get("vault_info", None))

    if request.method == "POST":
        vault_id = None
        if request.form["vault"] == "own_vault":
            if not session.get("vault_info", False):
                flash(
                    "Memory could not be uploaded.\
                          You cannot upload memories to your own vault.",
                    "warning")
                return render_template('memory_upload.html',
                                       title="Homepage",
                                       user=session["user_info"],
                                       vault=session.get("vault_info", None))

            vault_id = session.get("vault_info")["vault_id"]
        elif request.form["vault"] == "family_vault":
            if not session.get("family_vault_info", False):
                flash(
                    "Memory could not be uploaded.\
                          You cannot upload memories to your own vault.",
                    "warning")
                return render_template('memory_upload.html',
                                       title="Homepage",
                                       user=session["user_info"],
                                       vault=session.get("vault_info", None))

            vault_id = session.get("family_vault_info")["vault_id"]

        latitude = request.form.get("latitude", None)
        longitude = request.form.get("longitude", None)

        MemoryManagement.upload_memory(description=request.form["description"],
                                       date=request.form["date"],
                                       latitude=latitude if latitude != '' else None,
                                       longitude=longitude if longitude != '' else None,
                                       image_file=request.files.get("image"),
                                       vault_id=vault_id)

        return render_template('memory_upload.html',
                               title="Homepage",
                               user=session["user_info"],
                               vault=session["vault_info"])
