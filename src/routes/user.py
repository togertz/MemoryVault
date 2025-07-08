from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify

from ..services import UserManagement

user_bp = Blueprint('user', __name__, url_prefix="/u")

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if UserManagement.check_login(username=username,
                                      password=password):
            flash("Successfully logged in", "success")
            return render_template('login.html', title="Login")

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
        UserManagement.create_user(username=request.form["username"],
                                   password=request.form["password"],
                                   firstname=request.form["firstname"],
                                   lastname=request.form["lastname"],
                                   birthday=request.form["birthday"])

        return render_template("login.html", title="Login", register="True")

@user_bp.route("/username-taken", methods=["GET"])
def username_taken():
    username = request.args.get("username")

    return jsonify({"exists": UserManagement.username_taken(username)})
