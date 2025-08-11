"""
Module containing HTTP routes for memory upload.
Defines blueprint and logic for handeling requests to /memory url.
"""
import logging
import traceback
from datetime import datetime
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from ..services import MemoryManagement

memory_bp = Blueprint('memory', __name__, url_prefix='/memory')


@memory_bp.route('/', methods=["GET", "POST"])
def upload():
    """
    Handles GET and POST requests to url + /memory.

    Redirects to:
    - login if user is not authenticated
    - settings if neither private nor family vault is configured
    Answers GET requests with HTML render of upload page.
    Answers POST requests by creating memory.

    Returns:
        Reponse: A redirect or rendered template for memory upload.
    """
    # -- Check if user is already logged in --
    if not session.get("user_id", False):
        flash("Please login first", "warning")
        return redirect(url_for("user.login"))

    try:
        # -- Check if user already has configured family or private vault --
        if not session.get("vault_info", False) and not session.get("family_vault_info", False):
            return redirect(url_for("settings.index"))

        # -- Answer GET request by rendering upload template --
        if request.method == "GET":
            return render_template('memory_upload.html',
                                   title="Homepage",
                                   user=session["user_info"],
                                   vault=session.get("vault_info", None))

        # -- Answering POST request by creating memory --
        if request.method == "POST":
            vault_id = None

            # -- Get vault id for private or family vault depending on request input --
            if request.form["vault"] == "own_vault":
                if not session.get("vault_info", False):
                    flash(
                        "Memory could not be uploaded.\
                            You cannot upload memories to your own vault when it is not configured.",
                        "warning")
                    return render_template('memory_upload.html',
                                           title="Homepage",
                                           user=session["user_info"],
                                           vault=session.get("vault_info", None))

                vault_id = session.get("vault_info")["vault_id"]
                collection_period_start = datetime.strptime(session.get(
                    "vault_info")["curr_period_start"], "%A, %b %d, %Y").date()
                collection_period_end = datetime.strptime(session.get(
                    "vault_info")["curr_period_end"], "%A, %b %d, %Y").date()
            elif request.form["vault"] == "family_vault":
                if not session.get("family_vault_info", False):
                    flash(
                        "Memory could not be uploaded.\
                        You cannot upload memories to your family vault when it is not configured.",
                        "warning")
                    return render_template('memory_upload.html',
                                           title="Homepage",
                                           user=session["user_info"],
                                           vault=session.get("vault_info", None))

                vault_id = session.get("family_vault_info")["vault_id"]
                collection_period_start = datetime.strptime(session.get(
                    "family_vault_info")["curr_period_start"], "%A, %b %d, %Y").date()
                collection_period_end = datetime.strptime(session.get(
                    "family_vault_info")["curr_period_end"], "%A, %b %d, %Y").date()
            else:
                flash("Memory could not be uploaded.\
                    You have to chose a vault to upload.",
                      "warning")
                return render_template('memory_upload.html',
                                       title="Homepage",
                                       user=session["user_info"],
                                       vault=session.get("vault_info", None))

            memory_date = datetime.strptime(
                request.form["date"], "%Y-%m-%d").date()
            # -- Check if memory is in current collection period --
            if collection_period_start > memory_date or collection_period_end < memory_date:
                flash("Memory could not be uploaded.\
                    You cannot upload a memory that is not part of the current Collection Period",
                      "warning")
                return render_template('memory_upload.html',
                                       title="Homepage",
                                       user=session["user_info"],
                                       vault=session.get("vault_info", None))
            logging.info(
                f"User {session.get('user_id', None)} uploaded a new memory.")
            # -- Get Coordinates --
            latitude = request.form.get("latitude", None)
            longitude = request.form.get("longitude", None)

            # -- Create memory --
            MemoryManagement.upload_memory(description=request.form["description"],
                                           date=request.form["date"],
                                           latitude=latitude if latitude != '' else None,
                                           longitude=longitude if longitude != '' else None,
                                           image_file=request.files.get(
                                               "image"),
                                           vault_id=vault_id)

            return render_template('memory_upload.html',
                                   title="Homepage",
                                   user=session["user_info"],
                                   vault=session["vault_info"])
    except Exception as e:
        logging.error("Something went wrong %s", traceback.format_exc())
        message = "Please contact an admin to get furhter insights into this error."
        if session.get("user_info", {}).get("is_admin", False):
            message = traceback.format_exc()
        return render_template("base.html", user=session["user_info"], error=message)
