from flask import Blueprint, flash, redirect, render_template, request, url_for

from auth import current_user, login_required, require_role
from models import Update, db

updates_bp = Blueprint("updates", __name__)


@updates_bp.route("/updates")
@login_required
def list_view():
    updates = Update.query.order_by(Update.created_at.desc()).all()
    return render_template("updates.html", user=current_user(), updates=updates)


@updates_bp.route("/updates/add", methods=["POST"])
@require_role("admin")
def add():
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    if not title or not content:
        flash("Tytuł i treść są wymagane.", "error")
    else:
        db.session.add(Update(title=title, content=content))
        db.session.commit()
        flash("Dodano nową aktualność.", "success")
    return redirect(url_for("updates.list_view"))
