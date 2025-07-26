from flask import Blueprint, render_template, request, session, redirect, url_for, flash

slideshow_bp = Blueprint('slideshow', __name__, url_prefix='/slideshow')

@slideshow_bp.route('/', methods=["GET"])
def index():
    if not session.get("user_id", False):
        flash("Please login first", "warning")
        return redirect(url_for("user.login"))

    slideshow_info = {
        "available": True,
        "days_left": session["vault_info"]["days_left"],
        "period_end": session["vault_info"]["curr_period_end"]
    }

    return render_template("slideshow.html", user=session["user_html_package"], slideshow_info=slideshow_info)

@slideshow_bp.route('/run', methods=["GET"])
def start_slideshow():
    return render_template("slide.html", user=session["user_html_package"])