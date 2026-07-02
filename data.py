from datetime import datetime

# 1. PRYWATNA BAZA DANYCH (Lokalna struktura JSON - gotowa do migracji na Google Sheets API / SQLite)
DATABASE = {
    "students": [
        {"id": "S1001", "name": "Jan Kowalski", "status": "Enquiry", "recruiter": "Aleks"},
        {"id": "S1002", "name": "Anna Nowak", "status": "Application Submitted", "recruiter": "Aleks"},
        {"id": "S1003", "name": "Piotr Zieliński", "status": "Assessment Booked", "recruiter": "Marta"},
        {"id": "S1004", "name": "Maria Wiśniewska", "status": "Offer Accepted", "recruiter": "Tomasz"},
        {"id": "S1005", "name": "Krzysztof Wójcik", "status": "Enrolled", "recruiter": "Marta"},
        {"id": "S1006", "name": "Magdalena Kamińska", "status": "Missing Documents", "recruiter": "Aleks"},
        {"id": "S1007", "name": "Michał Lewandowski", "status": "Assessment Failed", "recruiter": "Tomasz"},
        {"id": "S1008", "name": "Agnieszka Włodarczyk", "status": "Additional Information Required", "recruiter": "Marta"},
        {"id": "S1009", "name": "Łukasz Podolski", "status": "Offer Received", "recruiter": "Aleks"},
        {"id": "S1010", "name": "Barbara Kwarc", "status": "Withdrawn", "recruiter": "Tomasz"},
        {"id": "S1011", "name": "Paweł Zarzeczny", "status": "Ineligible", "recruiter": "Marta"},
        {"id": "S1012", "name": "Katarzyna Figura", "status": "Incomplete Enrolment", "recruiter": "Aleks"},
        {"id": "S1013", "name": "Tomasz Kot", "status": "Assessment Missed", "recruiter": "Tomasz"},
        {"id": "S1014", "name": "Karolina Gruszka", "status": "Enquiry", "recruiter": "Marta"},
        {"id": "S1015", "name": "Marcin Dorociński", "status": "Application Submitted", "recruiter": "Tomasz"},
        {"id": "S1016", "name": "Natalia Kukulska", "status": "Offer Accepted", "recruiter": "Aleks"},
        {"id": "S1017", "name": "Robert Więckiewicz", "status": "Enrolled", "recruiter": "Aleks"},
        {"id": "S1018", "name": "Alicja Bachleda", "status": "Assessment Booked", "recruiter": "Marta"},
        {"id": "S1019", "name": "Dawid Podsiadło", "status": "Enquiry", "recruiter": "Tomasz"},
        {"id": "S1020", "name": "Sanah Jura", "status": "Offer Received", "recruiter": "Marta"}
    ],
    "updates": [
        {"title": "Welcome to ZochAI-CRM", "content": "Welcome to the ZochAI-CRM", "date": "2.07.2026"}
    ]
}

ALL_STATUSES = [
    "Enquiry", "Application Submitted", "Assessment Booked", "Assessment Missed",
    "Assessment Failed", "Missing Documents", "Additional Information Required",
    "Offer Received", "Offer Accepted", "Enrolled", "Ineligible", "Incomplete Enrolment", "Withdrawn"
]


def get_all_students():
    return DATABASE["students"]


def get_student_by_id(student_id):
    return next((s for s in DATABASE["students"] if s["id"] == student_id), None)


def user_can_edit_student(user, student):
    if student is None:
        return False
    if user["role"] == "admin":
        return True
    return student["recruiter"] == user["recruiter_name"]


def update_student_status(student_id, new_status):
    if new_status not in ALL_STATUSES:
        return False
    student = get_student_by_id(student_id)
    if student is None:
        return False
    student["status"] = new_status
    return True


def get_students_for_user(user):
    if user["role"] == "admin":
        return get_all_students()
    return [s for s in DATABASE["students"] if s["recruiter"] == user["recruiter_name"]]


def get_updates():
    return DATABASE["updates"]


def add_update(title, content):
    now = datetime.now()
    date_str = f"{now.day}.{now.month:02d}.{now.year}"
    DATABASE["updates"].insert(0, {"title": title, "content": content, "date": date_str})


def compute_stats(students):
    return {
        "total": len(students),
        "enquiry": len([s for s in students if s["status"] == "Enquiry"]),
        "booked": len([s for s in students if s["status"] == "Assessment Booked"]),
        "accepted": len([s for s in students if s["status"] == "Offer Accepted"]),
        "enrolled": len([s for s in students if s["status"] == "Enrolled"]),
    }


def compute_pipeline_counts(students):
    return {status: len([s for s in students if s["status"] == status]) for status in ALL_STATUSES}
