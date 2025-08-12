"""
Module containing HTTP routes for slideshow.
Defines blueprint and logic for handeling requests to /slideshow url.
"""
import os
import base64
import logging
import traceback
from datetime import datetime
from flask import Blueprint, render_template, \
    request, session, redirect, url_for, flash, current_app

from ..services import MemoryManagement, SlideshowModes, VaultManagement

slideshow_bp = Blueprint('slideshow', __name__, url_prefix='/slideshow')


@slideshow_bp.route('/', methods=["GET"])
def index():
    """
    Handles GET requests to url + /slideshow.

    Loads necessary vault information to display different slideshow options to the user.
    Depending on the collection period duration and admin status, the user can choose
    different options to view his slideshow.

    Returns:
        Response: Rendered template for slideshow page.
    """
    # -- Check if user is already logged in --
    if not session.get("user_id", False):
        flash("Please login first", "warning")
        return redirect(url_for("user.login"))
    try:
        # -- Check if user has private vault with a finished collection period to view --
        vault_slideshow_available = False
        vault_collection_periods = None
        if session.get("vault_info", False):
            # -- Get all existing periods of vault --
            vault_collection_periods = VaultManagement.get_all_periods(
                vault_id=session["vault_info"]["vault_id"])
            # -- If not admin: is there one closed period --
            vault_slideshow_available = len(vault_collection_periods) > 0\
                if session["user_info"]["admin"] else len(vault_collection_periods) > 1

        # -- Check if user has family vault with a finished collection period to view --
        family_slideshow_available = False
        family_collection_periods = None
        if session.get("family_vault_info", False):
            # -- Get all existing periods of vault --
            family_collection_periods = VaultManagement.get_all_periods(
                vault_id=session["family_vault_info"]["vault_id"])
            # -- If not admin: is there one closed period --
            family_slideshow_available = len(family_collection_periods) > 0\
                if session["user_info"]["admin"] else len(family_collection_periods) > 1

        slideshow_info = {
            "available": vault_slideshow_available or family_slideshow_available
        }

        # -- Remove current period as slideshow option if user has no admin privileges --
        if not session.get("user_info", {}).get("admin", False):
            if vault_slideshow_available:
                vault_collection_periods.pop(-1)
            if family_slideshow_available:
                family_collection_periods.pop(-1)

        # -- Load necessary slideshow information
        if vault_slideshow_available:
            slideshow_info["vault"] = {
                "periods": vault_collection_periods[::-1]
            }
        else:
            slideshow_info["vault"] = None
        if family_slideshow_available:
            slideshow_info["family"] = {
                "periods": family_collection_periods[::-1]
            }
        else:
            slideshow_info["family"] = None

        return render_template("slideshow.html",
                               user=session["user_info"],
                               slideshow_info=slideshow_info)
    except Exception as e:
        logging.error("Something went wrong %s", traceback.format_exc())
        message = "Please contact an admin to get furhter insights into this error."
        if session.get("user_info", {}).get("is_admin", False):
            message = traceback.format_exc()
        return render_template("base.html", user=session["user_info"], error=message)


@slideshow_bp.route('/run', methods=["GET", "POST"])
def start_slideshow():
    """
    Handles GET and POST requests to url + /slideshow/run for navigating through slideshow.

    Loads and renders memories for slideshow mode.
    POST requests will be triggered to start slideshow,
    while GET requests are used for navigating through slideshow.

    Returns:
        Response: Rendered template for memory.
    """
    # -- Check if user is already logged in --
    if not session.get("user_id", False):
        flash("Please login first", "warning")
        return redirect(url_for("user.login"))

    try:
        # -- Logic for starting slideshow --
        if request.method == "POST":
            # -- Getting vault id for slideshow vault --
            logging.info(
                f"User {session.get('user_id', None)} is accessing the slideshow.")
            vault_id = None
            if request.form.get("vault") == "own_vault":
                vault_id = session["vault_info"]["vault_id"]
            elif request.form.get("vault") == "family_vault":
                vault_id = session["family_vault_info"]["vault_id"]

            # -- Parse slideshow options --
            order = SlideshowModes(request.form.get("order"))
            period = request.form.get("collection-period").split("-")
            period_start = datetime.strptime(period[0], "%A, %b %d, %Y").date()
            period_end = datetime.strptime(period[1], "%A, %b %d, %Y").date()

            # -- Get slideshow order --
            session["slideshow_order"] = MemoryManagement.get_slideshow_order(vault_id=vault_id,
                                                                              order=order,
                                                                              period_start=period_start,
                                                                              period_end=period_end)

            if len(session["slideshow_order"]) <= 0:
                flash("No memories were found for this collection period", "warning")
                return redirect(url_for("slideshow.index"))

            current_memory = 1

        # -- Logic for navigating through slideshow --
        elif request.method == "GET":
            current_memory = int(request.args.get("number", 1))
            memory_order = session["slideshow_order"]

            if current_memory >= len(memory_order):
                current_memory = len(memory_order)
            elif current_memory < 1:
                current_memory = 1

        # -- Logic for displaying memories --
        memory_data = MemoryManagement.get_memory_data(
            memory_id=session["slideshow_order"][current_memory - 1])
        image_b64 = None

        if memory_data["image_uri"]:
            image_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"], memory_data["image_uri"])

            with open(image_path, "rb") as img_file:
                image_b64 = base64.b64encode(img_file.read()).decode("utf-8")

        display_memory_info = {
            "index": current_memory,
            "number_memories": len(session["slideshow_order"]),
            "date": memory_data["date"].strftime("%A, %b %d, %Y"),
            "description": memory_data["description"],
            "image_b64": image_b64 if image_b64 else None,
            "latitude": memory_data["latitude"] if memory_data["latitude"] else None,
            "longitude": memory_data["longitude"] if memory_data["longitude"] else None
        }

        return render_template("slide.html", user=session["user_info"], memory=display_memory_info)

    except Exception as e:
        logging.error("Something went wrong %s", traceback.format_exc())
        message = "Please contact an admin to get furhter insights into this error."
        if session.get("user_info", {}).get("is_admin", False):
            message = traceback.format_exc()
        return render_template("base.html", user=session["user_info"], error=message)
