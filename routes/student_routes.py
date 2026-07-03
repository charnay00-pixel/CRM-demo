from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for

from auth import current_user, login_required, require_role
from models import (
    APPLICATION_STATUSES,
    Application,
    Course,
    Student,
    User,
    db,
)
from permissions import (
    get_students_for_user,
    user_can_edit_application,
    user_can_edit_student,
)

students_bp = Blueprint("students", __name__)


@students_bp.route("/students")
@login_required
def list_view():
    user = current_user()
    return render_template(
        "students.html", user=user, students=get_students_for_user(user)
    )


@students_bp.route("/students/add", methods=["GET", "POST"])
@require_role("admin", "consultant")
def add():
    user = current_user()
    consultants = User.query.filter_by(role="consultant").order_by(User.display_name).all()
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        if not full_name:
            flash("Imię i nazwisko jest wymagane.", "error")
        else:
            if user.role == "admin":
                consultant_id = request.form.get("consultant_id", type=int)
            else:
                consultant_id = user.id  # consultant: zawsze auto-przypisanie do siebie
            dob_raw = request.form.get("date_of_birth", "")
            student = Student(
                full_name=full_name,
                phone=request.form.get("phone", "").strip() or None,
                email=request.form.get("email", "").strip() or None,
                date_of_birth=date.fromisoformat(dob_raw) if dob_raw else None,
                nationality=request.form.get("nationality", "").strip() or None,
                address=request.form.get("address", "").strip() or None,
                postcode=request.form.get("postcode", "").strip() or None,
                consultant_id=consultant_id,
            )
            db.session.add(student)
            db.session.commit()
            flash(f"Dodano studenta {student.full_name}.", "success")
            return redirect(url_for("students.detail", student_id=student.id))
    return render_template("student_form.html", user=user, consultants=consultants)


@students_bp.route("/students/<int:student_id>")
@login_required
def detail(student_id):
    user = current_user()
    student = db.get_or_404(Student, student_id)
    if user.role == "consultant" and student.consultant_id != user.id:
        flash("Nie masz uprawnień do podglądu tego studenta.", "error")
        return redirect(url_for("students.list_view"))
    courses = Course.query.order_by(Course.name).all()
    return render_template(
        "student_detail.html",
        user=user,
        student=student,
        courses=courses,
        application_statuses=APPLICATION_STATUSES,
        can_edit=user_can_edit_student(user, student),
    )


@students_bp.route("/students/<int:student_id>/applications/add", methods=["POST"])
@login_required
def add_application(student_id):
    user = current_user()
    student = db.get_or_404(Student, student_id)
    if not user_can_edit_student(user, student):
        flash("Nie masz uprawnień do edycji tego studenta.", "error")
        return redirect(url_for("students.list_view"))

    course = db.session.get(Course, request.form.get("course_id", type=int) or 0)
    if course is None:
        flash("Wybierz prawidłowy kurs.", "error")
        return redirect(url_for("students.detail", student_id=student.id))

    application = Application(
        student=student,
        university=course.university,
        campus=course.campus,
        course=course,
        intake=request.form.get("intake", "").strip() or None,
        study_mode=course.study_mode,
        status="Draft",
        application_date=date.today(),
        submitted_by_id=user.id,
    )
    db.session.add(application)
    db.session.commit()
    flash(f"Dodano aplikację na {course.name} ({course.campus.name}).", "success")
    return redirect(url_for("students.detail", student_id=student.id))


@students_bp.route("/applications/<int:application_id>/status", methods=["POST"])
@login_required
def update_application_status(application_id):
    user = current_user()
    application = db.session.get(Application, application_id)

    if not user_can_edit_application(user, application):
        flash("Nie masz uprawnień do edycji tej aplikacji.", "error")
        return redirect(url_for("students.list_view"))

    new_status = request.form.get("status", "")
    if new_status not in APPLICATION_STATUSES:
        flash("Nieprawidłowy status.", "error")
    else:
        application.status = new_status
        db.session.commit()
        flash(
            f"Zaktualizowano status aplikacji studenta {application.student.full_name}.",
            "success",
        )
    return redirect(url_for("students.detail", student_id=application.student_id))


@students_bp.route("/applications")
@login_required
def application_list():
    user = current_user()
    students = get_students_for_user(user)
    applications = [a for s in students for a in s.applications]

    status_filter = request.args.get("status", "")
    if status_filter in APPLICATION_STATUSES:
        applications = [a for a in applications if a.status == status_filter]

    applications.sort(key=lambda a: a.created_at, reverse=True)
    return render_template(
        "applications.html",
        user=user,
        applications=applications,
        application_statuses=APPLICATION_STATUSES,
        selected_status=status_filter,
    )
