import os
import base64
from datetime import datetime
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app

from ..services import MemoryManagement, SlideshowModes, VaultManagement

slideshow_bp = Blueprint('slideshow', __name__, url_prefix='/slideshow')

@slideshow_bp.route('/', methods=["GET"])
def index():
    if not session.get("user_id", False):
        flash("Please login first", "warning")
        return redirect(url_for("user.login"))

    slideshow_info = {
        "available": True,
        "days_left": session["vault_info"]["days_left"],
        "period_start": session["vault_info"]["curr_period_start"],
        "period_end": session["vault_info"]["curr_period_end"],
        "previous_periods": VaultManagement.get_all_periods(session["vault_info"]["vault_id"])[::-1]
    }

    return render_template("slideshow.html", user=session["user_info"], slideshow_info=slideshow_info)

@slideshow_bp.route('/run', methods=["GET", "POST"])
def start_slideshow():
    if not session.get("user_id", False):
        flash("Please login first", "warning")
        return redirect(url_for("user.login"))

    if not session["user_info"]["admin"]:
        if not session["vault_info"]["slideshow_available"]:
            return redirect(url_for("slideshow.index"))

    if request.method == "POST":
        order = SlideshowModes(request.form.get("order"))
        period = request.form.get("collection-period").split("-")
        period_start = datetime.strptime(period[0], "%A, %b %d, %Y").date()
        period_end = datetime.strptime(period[1], "%A, %b %d, %Y").date()

        session["slideshow_order"] = MemoryManagement.get_slideshow_order(session["vault_info"]["vault_id"],
                                                                order=order,
                                                                period_start=period_start,
                                                                period_end=period_end)

        if len(session["slideshow_order"]) <= 0:
            flash("No memories were found for this collection period")
            return redirect(url_for("slideshow.index"))

        current_memory = 1
    elif request.method == "GET":
        current_memory = int(request.args.get("number", 1))
        memory_order = session["slideshow_order"]

        if current_memory >= len(memory_order):
            current_memory = len(memory_order)
        elif current_memory < 1:
            current_memory = 1

    memory_data = MemoryManagement.get_memory_data(id=session["slideshow_order"][current_memory - 1])
    image_b64 = None

    if memory_data["image_uri"]:
        image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], memory_data["image_uri"])

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