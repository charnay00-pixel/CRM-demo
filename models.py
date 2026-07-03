from datetime import date, datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

# Słowniki wartości trzymane w kodzie (nie SQL Enum) — dodanie nowej wartości
# to zmiana jednej linijki bez migracji schematu.
ROLES = ["admin", "consultant", "finance", "viewer"]

ROLE_LABELS = {
    "admin": "System Administrator",
    "consultant": "Consultant",
    "finance": "Finance",
    "viewer": "Viewer",
}

UNIVERSITY_STATUSES = ["Active", "Pending", "Paused", "Closed", "Do not use"]
PARTNERSHIP_TYPES = ["Direct contract", "Via B2B partner", "Pending", "Not active"]

COURSE_LEVELS = ["Foundation", "CertHE", "HND", "Bachelor", "Top-Up", "Master"]
COURSE_CATEGORIES = [
    "Business", "Healthcare", "Law", "Psychology", "Computing",
    "Construction", "Accounting", "Marketing", "Education",
]
STUDY_MODES = ["Online", "Campus", "Hybrid"]

APPLICATION_STATUSES = [
    "Draft", "Missing documents", "Ready to submit", "Submitted",
    "Under review", "Interview required", "Interview booked", "Interview passed",
    "Conditional offer", "Unconditional offer", "Offer accepted",
    "Enrolment pending", "Enrolled", "Rejected", "Withdrawn", "Deferred",
]


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)  # jedna z ROLES
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    students: Mapped[list["Student"]] = relationship(
        back_populates="consultant", foreign_keys="Student.consultant_id"
    )


class University(db.Model):
    __tablename__ = "universities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    partnership_type: Mapped[str] = mapped_column(String(30), nullable=False, default="Direct contract")
    partner_agency_name: Mapped[str | None] = mapped_column(String(200))
    contact_person: Mapped[str | None] = mapped_column(String(120))
    contact_email: Mapped[str | None] = mapped_column(String(120))
    contact_phone: Mapped[str | None] = mapped_column(String(30))
    application_portal_url: Mapped[str | None] = mapped_column(String(300))
    application_form_url: Mapped[str | None] = mapped_column(String(300))
    documents_url: Mapped[str | None] = mapped_column(String(300))
    internal_notes: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Active")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    campuses: Mapped[list["Campus"]] = relationship(
        back_populates="university", cascade="all, delete-orphan"
    )
    courses: Mapped[list["Course"]] = relationship(
        back_populates="university", cascade="all, delete-orphan"
    )
    applications: Mapped[list["Application"]] = relationship(back_populates="university")


class Campus(db.Model):
    __tablename__ = "campuses"

    id: Mapped[int] = mapped_column(primary_key=True)
    university_id: Mapped[int] = mapped_column(ForeignKey("universities.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    address: Mapped[str | None] = mapped_column(String(300))
    city: Mapped[str | None] = mapped_column(String(100))
    postcode: Mapped[str | None] = mapped_column(String(20))
    nearest_station: Mapped[str | None] = mapped_column(String(150))
    study_modes: Mapped[str | None] = mapped_column(String(100))  # np. "Campus, Hybrid"
    place_limits: Mapped[str | None] = mapped_column(String(100))
    attendance_requirements: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)

    university: Mapped["University"] = relationship(back_populates="campuses")
    courses: Mapped[list["Course"]] = relationship(back_populates="campus")
    applications: Mapped[list["Application"]] = relationship(back_populates="campus")


class Course(db.Model):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    university_id: Mapped[int] = mapped_column(ForeignKey("universities.id"), nullable=False)
    campus_id: Mapped[int] = mapped_column(ForeignKey("campuses.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    level: Mapped[str] = mapped_column(String(20), nullable=False)      # COURSE_LEVELS
    category: Mapped[str] = mapped_column(String(30), nullable=False)   # COURSE_CATEGORIES
    duration: Mapped[str | None] = mapped_column(String(100))           # np. "3 lata"
    intakes: Mapped[str | None] = mapped_column(String(200))            # np. "September, January"
    study_mode: Mapped[str] = mapped_column(String(20), nullable=False, default="Campus")
    awarding_body: Mapped[str | None] = mapped_column(String(200))
    requirements: Mapped[str | None] = mapped_column(Text)
    career_outcomes: Mapped[str | None] = mapped_column(Text)
    internal_notes: Mapped[str | None] = mapped_column(Text)

    university: Mapped["University"] = relationship(back_populates="courses")
    campus: Mapped["Campus"] = relationship(back_populates="courses")
    applications: Mapped[list["Application"]] = relationship(back_populates="course")


class Student(db.Model):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(30))
    email: Mapped[str | None] = mapped_column(String(120))
    date_of_birth: Mapped[date | None] = mapped_column(Date)
    nationality: Mapped[str | None] = mapped_column(String(100))
    address: Mapped[str | None] = mapped_column(String(300))
    postcode: Mapped[str | None] = mapped_column(String(20))
    consultant_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    consultant: Mapped["User"] = relationship(
        back_populates="students", foreign_keys=[consultant_id]
    )
    applications: Mapped[list["Application"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )


class Application(db.Model):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    university_id: Mapped[int] = mapped_column(ForeignKey("universities.id"), nullable=False)
    campus_id: Mapped[int] = mapped_column(ForeignKey("campuses.id"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    intake: Mapped[str | None] = mapped_column(String(50))          # np. "September 2026"
    study_mode: Mapped[str | None] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="Draft")
    application_date: Mapped[date | None] = mapped_column(Date)
    submitted_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    application_ref: Mapped[str | None] = mapped_column(String(100))
    docs_received_date: Mapped[date | None] = mapped_column(Date)
    submitted_date: Mapped[date | None] = mapped_column(Date)
    interview_date: Mapped[date | None] = mapped_column(Date)
    offer_date: Mapped[date | None] = mapped_column(Date)
    enrolment_date: Mapped[date | None] = mapped_column(Date)
    course_start_date: Mapped[date | None] = mapped_column(Date)
    offer_details: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    student: Mapped["Student"] = relationship(back_populates="applications")
    university: Mapped["University"] = relationship(back_populates="applications")
    campus: Mapped["Campus"] = relationship(back_populates="applications")
    course: Mapped["Course"] = relationship(back_populates="applications")
    submitted_by: Mapped["User"] = relationship(foreign_keys=[submitted_by_id])


class Update(db.Model):
    __tablename__ = "updates"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
