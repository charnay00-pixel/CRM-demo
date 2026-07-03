from functools import wraps

from flask import flash, redirect, session, url_for
from werkzeug.security import check_password_hash

from models import User, db


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return db.session.get(User, user_id)


def verify_login(username, password):
    user = User.query.filter_by(username=username.lower()).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped


def require_role(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("auth.login"))
            user = current_user()
            if user is None or user.role not in roles:
                flash("Nie masz uprawnień do wykonania tej akcji.", "error")
                return redirect(url_for("dashboard.index"))
            return view(*args, **kwargs)

        return wrapped

    return decorator
