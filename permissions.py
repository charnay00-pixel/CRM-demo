from models import Student


def user_can_edit_student(user, student):
    if user is None or student is None:
        return False
    if user.role == "admin":
        return True
    if user.role == "consultant":
        return student.consultant_id == user.id
    return False  # finance, viewer: tylko odczyt


def user_can_edit_application(user, application):
    # Uprawnienie do aplikacji płynie przez studenta-właściciela.
    if application is None:
        return False
    return user_can_edit_student(user, application.student)


def get_students_for_user(user):
    if user.role in ("admin", "finance", "viewer"):
        return Student.query.order_by(Student.full_name).all()
    return (
        Student.query.filter_by(consultant_id=user.id)
        .order_by(Student.full_name)
        .all()
    )
