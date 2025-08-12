"""
Module containing HTTP routes for user page.
Defines blueprint and logic for handeling requests to /user url.
"""
import logging
import traceback
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session

from ..services import UserManagement, UserException, VaultManagement

user_bp = Blueprint('user', __name__, url_prefix="/u")


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles GET requests to url + /user/login.

    Renders login page and checks login information.

    Returns:
        Response: Rendered template for login page.
    """
    # -- Check if user is already logged in --
    if session.get("user_id", False):
        return redirect(url_for("memory.upload"))

    try:
        # -- Handle user login --
        if request.method == "POST":
            username = request.form.get("username").lower()
            password = request.form.get("password")

            user_id = UserManagement.check_login(username=username,
                                                 password=password)

            # -- Handle successful login and load user data into session --
            if user_id:
                session["user_id"] = user_id
                session["user_info"] = UserManagement.get_user_info(
                    user_id)
                session["vault_info"] = VaultManagement.get_vault_info(user_id)

                if session["user_info"].get("family_id", False):
                    session["family_vault_info"] = {
                        **UserManagement.get_family_info(
                            session["user_info"].get("family_id", False)),
                        **VaultManagement.get_vault_info(
                            family_id=session["user_info"].get("family_id", None)),
                        "number_memories": VaultManagement.get_number_memories(
                            family_id=session["user_info"].get("family_id", False))
                    }

                flash("Successfully logged in", "info")

                return redirect(url_for("memory.upload"))

            # -- Handle unsucessful login and render error message --
            if UserManagement.username_taken(username=username):
                flash("Wrong password", "warning")
            else:
                flash("User does not exist", "warning")
            return render_template("login.html", title="Login", username_value=username)

        # -- Render Login page --
        if request.method == "GET":
            return render_template('login.html', title="Login")

    except Exception as e:
        logging.error("Something went wrong %s", traceback.format_exc())
        message = "Please contact an admin to get furhter insights into this error."
        if session.get("user_info", {}).get("is_admin", False):
            message = traceback.format_exc()
        return render_template("base.html", user=session.get("user_info", None), error=message)


@user_bp.route("/logout", methods=["GET"])
def logout():
    """
    Handles GET requests to url + /user/logout.

    Handles user logout and clears session.

    Returns:
        Response: Rendered template for settings page.
    """
    # -- Check if user is already logged in --
    if not session.get("user_id", False):
        return redirect(url_for("user.login"))

    try:
        # -- Clear session --
        session.clear()
        flash("Successfully logged out", "success")
        return redirect(url_for("base.index"))

    except Exception as e:
        logging.error("Something went wrong %s", traceback.format_exc())
        message = "Please contact an admin to get furhter insights into this error."
        if session.get("user_info", {}).get("is_admin", False):
            message = traceback.format_exc()
        return render_template("base.html", user=session["user_info"], error=message)


@user_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Handles GET requests to url + /user/register.

    Renders register page and handles registration of new users.

    Returns:
        Response: Rendered template for login page.
    """
    # -- Check if user is already logged in --
    if session.get("user_id", False):
        return redirect(url_for("memory.upload"))

    # -- Render Register page --
    if request.method == "GET":
        return render_template("register.html", title="Register")

    # -- Handle registration --
    if request.method == "POST":
        try:
            UserManagement.create_user(username=request.form["username"],
                                       password=request.form["password"],
                                       password_repeat=request.form["password-repeat"],
                                       firstname=request.form["firstname"],
                                       lastname=request.form["lastname"],
                                       birthday=request.form["birthday"],
                                       admin_token=request.form.get("admin-token", None))

            return render_template("login.html", title="Login", register="True")
        except UserException as e:
            flash(e.get_message(), "warning")
            return render_template("register.html", title="Register")
        except Exception as e:
            logging.error("Something went wrong %s", traceback.format_exc())
            message = "Please contact an admin to get furhter insights into this error."
            if session.get("user_info", {}).get("is_admin", False):
                message = traceback.format_exc()
            return render_template("base.html", user=session.get("user_info", None), error=message)


@user_bp.route("/username-taken", methods=["GET"])
def username_taken() -> dict:
    """
    Handles GET requests to url + /user/username-taken.

    Returns json object containing information whether username is already taken.
    Is used by registration page for dynamically displaying whether username can be used.

    Returns:
        dicts: Containing flag whether or not username already exists.
    """
    username = request.args.get("username")

    return jsonify({"exists": UserManagement.username_taken(username)})
