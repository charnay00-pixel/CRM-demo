from functools import wraps

from flask import flash, redirect, session, url_for

from users import get_user


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        user = current_user()
        if user is None or user["role"] != "admin":
            flash("Nie masz uprawnień do wykonania tej akcji.", "error")
            return redirect(url_for("updates"))
        return view(*args, **kwargs)

    return wrapped


def current_user():
    username = session.get("username")
    if not username:
        return None
    return get_user(username)
