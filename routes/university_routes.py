from flask import Blueprint, flash, redirect, render_template, request, url_for

from auth import current_user, login_required, require_role
from models import (
    COURSE_CATEGORIES,
    COURSE_LEVELS,
    PARTNERSHIP_TYPES,
    UNIVERSITY_STATUSES,
    Campus,
    Course,
    University,
    db,
)

universities_bp = Blueprint("universities", __name__)


@universities_bp.route("/universities")
@login_required
def list_view():
    universities = University.query.order_by(University.name).all()
    return render_template(
        "universities.html", user=current_user(), universities=universities
    )


@universities_bp.route("/universities/add", methods=["GET", "POST"])
@require_role("admin")
def add():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        partnership_type = request.form.get("partnership_type", "")
        status = request.form.get("status", "")
        if not name:
            flash("Nazwa uczelni jest wymagana.", "error")
        elif partnership_type not in PARTNERSHIP_TYPES or status not in UNIVERSITY_STATUSES:
            flash("Nieprawidłowy typ współpracy lub status.", "error")
        else:
            university = University(
                name=name,
                partnership_type=partnership_type,
                status=status,
                partner_agency_name=request.form.get("partner_agency_name", "").strip() or None,
                contact_person=request.form.get("contact_person", "").strip() or None,
                contact_email=request.form.get("contact_email", "").strip() or None,
                contact_phone=request.form.get("contact_phone", "").strip() or None,
                application_portal_url=request.form.get("application_portal_url", "").strip() or None,
                internal_notes=request.form.get("internal_notes", "").strip() or None,
            )
            db.session.add(university)
            db.session.commit()
            flash(f"Dodano uczelnię {university.name}.", "success")
            return redirect(url_for("universities.detail", university_id=university.id))
    return render_template(
        "university_form.html",
        user=current_user(),
        partnership_types=PARTNERSHIP_TYPES,
        university_statuses=UNIVERSITY_STATUSES,
    )


@universities_bp.route("/universities/<int:university_id>")
@login_required
def detail(university_id):
    university = db.get_or_404(University, university_id)
    return render_template(
        "university_detail.html", user=current_user(), university=university
    )


@universities_bp.route("/campuses/<int:campus_id>")
@login_required
def campus_detail(campus_id):
    campus = db.get_or_404(Campus, campus_id)
    return render_template("campus_detail.html", user=current_user(), campus=campus)


@universities_bp.route("/courses")
@login_required
def course_list():
    query = Course.query
    university_id = request.args.get("university_id", type=int)
    category = request.args.get("category", "")
    level = request.args.get("level", "")
    if university_id:
        query = query.filter_by(university_id=university_id)
    if category in COURSE_CATEGORIES:
        query = query.filter_by(category=category)
    if level in COURSE_LEVELS:
        query = query.filter_by(level=level)
    courses = query.order_by(Course.name).all()
    return render_template(
        "courses.html",
        user=current_user(),
        courses=courses,
        universities=University.query.order_by(University.name).all(),
        course_categories=COURSE_CATEGORIES,
        course_levels=COURSE_LEVELS,
        selected_university_id=university_id,
        selected_category=category,
        selected_level=level,
    )


@universities_bp.route("/courses/<int:course_id>")
@login_required
def course_detail(course_id):
    course = db.get_or_404(Course, course_id)
    return render_template("course_detail.html", user=current_user(), course=course)
