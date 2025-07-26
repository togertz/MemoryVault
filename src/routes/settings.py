from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from ..services import UserManagement, VaultManagement

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route("/", methods=["GET"])
def index():
    if not session.get("user_id", False):
        flash("Please login first", "warning")
        return redirect(url_for("user.login"))

    vault_info = VaultManagement.get_vault_info(user_id=session.get("user_id", False))
    if vault_info:
        vault_info["number_memories"] = VaultManagement.get_number_memories(user_id=session.get("user_id", None))
    session["vault_info"] = vault_info

    return render_template("settings.html", user=session["user_info"], vault=session.get("vault_info", None))

@settings_bp.route("/create_vault", methods=["POST"])
def create_vault():
    if request.method == "POST":
        try:
            if session.get("vault_info", False):
                flash("You already created a vault", "warning")
                return redirect(url_for("settings.index"))

            VaultManagement.create_vault(user_id=session["user_id"],
                                        period_duration=request.form["duration"],
                                        first_period_start=request.form["start"])

            session["vault_info"] = VaultManagement.get_vault_info(session["user_id"])

            return render_template("settings.html", user=session["user_info"], vault=session.get("vault_info", None))
        except Exception as e:
            raise e
            flash("Something went wrong", "error")
            return render_template("settings.html", user=session["user_id"], vault=session.get("vault_info", None))