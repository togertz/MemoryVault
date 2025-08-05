"""
Module containing HTTP routes for settings page.
Defines blueprint and logic for handeling requests to /settings url.
"""
import traceback
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from ..services import UserManagement, VaultManagement, UserException

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')


@settings_bp.route("/", methods=["GET"])
def index():
    """
    Handles GET requests to url + /settings.

    Loads necessary information and renders settings page to user.

    Returns:
        Response: Rendered template for settings page.
    """
    # -- Check if user is already logged in --
    if not session.get("user_id", False):
        flash("Please login first", "warning")
        return redirect(url_for("user.login"))

    try:
        # -- Load information for private vault --
        vault_info = VaultManagement.get_vault_info(
            user_id=session.get("user_id", False))
        if vault_info:
            vault_info["number_memories"] = VaultManagement.get_number_memories(
                user_id=session.get("user_id", None))
        session["vault_info"] = vault_info

        # -- Load information for family vault.
        family_info = None
        if session["user_info"].get("family_id", False):
            family_info = session.get("family_vault_info")

        return render_template("settings.html",
                               user=session["user_info"],
                               vault=vault_info,
                               family_vault=family_info)

    except Exception:
        message = "Please contact an admin to get furhter insights into this error."
        if session.get("user_info").get("io_admin"):
            message = traceback.format_exc()
        return render_template("base.html", user=session["user_info"], error=message)


@settings_bp.route("/create_vault", methods=["POST"])
def create_vault():
    """
    Handles POST requests to url + /create_vault to create a configured vault for the user.

    Creates a vault and stores its information in db.

    Returns:
        Response: Rendered template for settings page containing vault information.
    """
    # -- Check if user is already logged in --
    if not session.get("user_id", False):
        flash("Please login first", "warning")
        return redirect(url_for("user.login"))

    if request.method == "POST":
        try:
            # -- Check if user already created a vault --
            if session.get("vault_info", False):
                flash("You already created a vault", "warning")
                return redirect(url_for("settings.index"))

            # -- Create vault --
            VaultManagement.create_vault(user_id=session["user_id"],
                                         family_id=None,
                                         period_duration=request.form["duration"],
                                         first_period_start=request.form["start"])

            session["vault_info"] = VaultManagement.get_vault_info(
                session["user_id"])

            return redirect(url_for("settings.index"))
        except Exception:
            flash("Something went wrong", "error")
            return render_template("settings.html",
                                   user=session["user_id"],
                                   vault=session.get("vault_info", None),
                                   family=session.get("family_vault_info", None))


@settings_bp.route("/join_family", methods=["POST"])
def join_family():
    """
    Handles POST requests to url + /join_family.

    Adds user as member of a family.

    Returns:
        Response: Rendered template for settings page containing family information.
    """
    if request.method == "POST":
        try:
            # -- Add user to family --
            family_id = UserManagement.join_family(
                user_id=session["user_id"], invite_code=request.form.get("invite-code", ""))

            # -- Load family information into session --
            session["user_info"] = UserManagement.get_user_info(
                session["user_id"])
            session["family_vault_info"] = {
                **UserManagement.get_family_info(family_id),
                **VaultManagement.get_vault_info(family_id=family_id),
                "number_memories": VaultManagement.get_number_memories(family_id=family_id)
            }

            flash("Successfully joined family", "info")
            return redirect(url_for("settings.index"))
        except UserException as e:
            flash(e.get_message(), "warning")
            return redirect(url_for("settings.index"))


@settings_bp.route("/create_family", methods=["POST"])
def create_family():
    """
    Handles POST requests to url + /create_family.

    Creates family with configured vault and adds user as member of a family.

    Returns:
        Response: Rendered template for settings page containing family information.
    """
    if request.method == "POST":
        try:
            # -- Check if user is already a member of a family --
            if session.get("family_vault_info", False):
                flash("You are already part of a family.", "warning")
                return redirect(url_for("settings.index"))

            # -- Create family and store in db --
            family_id = UserManagement.create_family(
                user_id=session["user_id"], family_name=request.form.get("family-name"))
            session["user_info"] = UserManagement.get_user_info(
                session["user_id"])
            session["family_info"] = UserManagement.get_family_info(
                family_id=family_id)

            VaultManagement.create_vault(user_id=None,
                                         family_id=session["user_info"]["family_id"],
                                         period_duration=request.form["duration"],
                                         first_period_start=request.form["start"])

            # -- Load family information into session --
            session["user_info"] = UserManagement.get_user_info(
                session["user_id"])
            session["family_vault_info"] = {
                **UserManagement.get_family_info(family_id),
                **VaultManagement.get_vault_info(family_id=family_id),
                "number_memories": VaultManagement.get_number_memories(family_id=family_id)
            }
            return redirect(url_for("settings.index"))
        except UserException as e:
            flash(e.get_message(), "warning")
            return redirect(url_for("settings.index"))


@settings_bp.route("/quit_family", methods=["POST"])
def quit_family():
    """
    Handles POST requests to url + /quit_family.

    Removes user as member of a family and clears session from family information.

    Returns:
        Response: Rendered template for settings page containing family information.
    """
    if request.method == "POST":
        if not session.get("family_vault_info", False):
            flash("You are not part of a family.", "warning")
            return redirect(url_for("settings.index"))
        try:
            UserManagement.quit_family(session["user_id"])
            session["user_info"] = UserManagement.get_user_info(
                session["user_id"])
            session.pop("family_vault_info")
            flash("Successfully quit family.", "info")
            return redirect(url_for("settings.index"))
        except UserException as e:
            flash(e.get_message(), "warning")
            return redirect(url_for("settings.index"))
