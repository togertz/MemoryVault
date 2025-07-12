from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session

from ..services import UserManagement, UserException

user_bp = Blueprint('user', __name__, url_prefix="/u")

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_id = UserManagement.check_login(username=username,
                                      password=password)

        if user_id:
            session["user_id"] = user_id
            flash(f"Successfully logged in - {session['user_id']}", "success")

            return redirect(url_for("memory.upload"))#render_template('login.html', title="Login")

        else:
            if UserManagement.username_taken(username=username):
                flash("Wrong password", "error")
            else:
                flash("User does not exist", "error")
            return render_template("login.html", title="Login", username_value=username)

    if request.method == "GET":
        return render_template('login.html', title="Login")

@user_bp.route("/register", methods=["GET", "POST"])
def register():
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
