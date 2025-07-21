from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session

from ..services import UserManagement, UserException, VaultManagement

user_bp = Blueprint('user', __name__, url_prefix="/u")

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id", False):
        return redirect(url_for("memory.upload"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_id = UserManagement.check_login(username=username,
                                      password=password)

        if user_id:
            session["user_id"] = user_id
            session["user_html_package"] = UserManagement.get_user_json_package(user_id)
            session["vault_info"] = VaultManagement.get_vault_info(user_id)
            flash(f"Successfully logged in", "success")

            return redirect(url_for("memory.upload"))#render_template('login.html', title="Login")

        else:
            if UserManagement.username_taken(username=username):
                flash("Wrong password", "error")
            else:
                flash("User does not exist", "error")
            return render_template("login.html", title="Login", username_value=username)

    if request.method == "GET":
        return render_template('login.html', title="Login")

@user_bp.route("/logout", methods=["GET"])
def logout():
    if not session.get("user_id", False):
        return redirect(url_for("user.login"))

    session.clear()
    flash("Successfully logged out", "success")
    return redirect(url_for("base.index"))

@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id", False):
        return redirect(url_for("memory.upload"))

    if request.method == "GET":
        return render_template("register.html", title="Register")

    if request.method == "POST":
        try:
            UserManagement.create_user(username=request.form["username"],
                                       password=request.form["password"],
                                       password_repeat=request.form["password-repeat"],
                                       firstname=request.form["firstname"],
                                       lastname=request.form["lastname"],
                                       birthday=request.form["birthday"])

            return render_template("login.html", title="Login", register="True")
        except UserException as e:
            flash(e.get_message(), "warning")
            return render_template("register.html", title="Register")


@user_bp.route("/username-taken", methods=["GET"])
def username_taken():
    username = request.args.get("username")

    return jsonify({"exists": UserManagement.username_taken(username)})
