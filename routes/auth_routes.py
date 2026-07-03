from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from auth import verify_login

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        user = verify_login(username, password)
        if user:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("dashboard.index"))
        flash("Nieprawidłowa nazwa użytkownika lub hasło.", "error")
        return render_template("login.html")
    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
