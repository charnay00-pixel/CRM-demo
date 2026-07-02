import os

from flask import Flask, flash, redirect, render_template, request, session, url_for

from auth import admin_required, current_user, login_required
from data import (
    ALL_STATUSES,
    add_update,
    compute_pipeline_counts,
    compute_stats,
    get_student_by_id,
    get_students_for_user,
    get_updates,
    update_student_status,
    user_can_edit_student,
)
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
        flash("Nieprawidłowa nazwa użytkownika lub hasło.", "error")
        return render_template("login.html")
    return render_template("login.html")


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


@app.route("/students")
@login_required
def students():
    user = current_user()
    return render_template(
        "students.html",
        user=user,
        students=get_students_for_user(user),
        all_statuses=ALL_STATUSES,
    )


@app.route("/students/<student_id>/status", methods=["POST"])
@login_required
def update_status(student_id):
    user = current_user()
    student = get_student_by_id(student_id)

    if not user_can_edit_student(user, student):
        flash("Nie masz uprawnień do edycji tego ucznia.", "error")
        return redirect(url_for("students"))

    new_status = request.form.get("status", "")
    if update_student_status(student_id, new_status):
        flash(f"Zaktualizowano status ucznia {student['name']}.", "success")
    else:
        flash("Nieprawidłowy status.", "error")
    return redirect(url_for("students"))


@app.route("/updates")
@login_required
def updates():
    user = current_user()
    return render_template("updates.html", user=user, updates=get_updates())


@app.route("/updates/add", methods=["POST"])
@login_required
@admin_required
def add_update_route():
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    if not title or not content:
        flash("Tytuł i treść są wymagane.", "error")
    else:
        add_update(title, content)
        flash("Dodano nową aktualność.", "success")
    return redirect(url_for("updates"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("--- SmartEd CRM uruchomiony pomyślnie! ---")
    print(f"Otwórz w przeglądarce: http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
