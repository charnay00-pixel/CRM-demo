import os

from flask import Flask, redirect, render_template, request, session, url_for

from auth import current_user, login_required
from data import compute_pipeline_counts, compute_stats, get_students_for_user, get_updates
from users import verify_login

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-insecure-key-change-me")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        user = verify_login(username, password)
        if user:
            session.clear()
            session["username"] = user["username"]
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Nieprawidłowa nazwa użytkownika lub hasło.")
    return render_template("login.html", error=None)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def dashboard():
    user = current_user()
    students = get_students_for_user(user)
    return render_template(
        "dashboard.html",
        user=user,
        stats=compute_stats(students),
        pipeline_counts=compute_pipeline_counts(students),
        updates=get_updates(),
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("--- SmartEd CRM uruchomiony pomyślnie! ---")
    print(f"Otwórz w przeglądarce: http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
