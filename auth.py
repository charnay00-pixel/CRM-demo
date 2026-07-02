from functools import wraps

from flask import redirect, session, url_for

from users import get_user


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def current_user():
    username = session.get("username")
    if not username:
        return None
    return get_user(username)
