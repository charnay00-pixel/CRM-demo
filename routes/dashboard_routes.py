from flask import Blueprint, render_template

from auth import current_user, login_required
from models import APPLICATION_STATUSES, University, Update
from permissions import get_students_for_user

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    user = current_user()
    students = get_students_for_user(user)
    applications = [a for s in students for a in s.applications]

    stats = {
        "students": len(students),
        "applications": len(applications),
        "universities": University.query.count(),
        "enrolled": len([a for a in applications if a.status == "Enrolled"]),
    }
    pipeline_counts = {
        status: len([a for a in applications if a.status == status])
        for status in APPLICATION_STATUSES
    }
    latest_update = Update.query.order_by(Update.created_at.desc()).first()

    return render_template(
        "dashboard.html",
        user=user,
        stats=stats,
        pipeline_counts=pipeline_counts,
        latest_update=latest_update,
    )
