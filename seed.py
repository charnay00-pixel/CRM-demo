# UWAGA (persystencja): na darmowym planie Render dysk jest efemeryczny —
# plik instance/crm.db znika przy każdym redeployu/restarcie instancji,
# więc dane wracają do stanu seedowego. To świadome ograniczenie tej iteracji
# (tak jak wcześniej dict w pamięci); trwały magazyn to osobny, przyszły krok.
from datetime import date

from models import (
    Application,
    Campus,
    Course,
    Student,
    University,
    Update,
    User,
    db,
)


def init_db(app):
    with app.app_context():
        db.create_all()
        if User.query.count() == 0:
            _seed_users()
        if University.query.count() == 0:
            _seed_core_demo_data()
        db.session.commit()


def _seed_users():
    # Alexa — jedyne realne konto (admin). Marta i Tomasz to zaślepki testowe
    # do weryfikacji filtrowania/uprawnień per-konsultant.
    users = [
        User(
            username="alexa",
            password_hash="scrypt:32768:8:1$D3BDmkiq0GA2xHEr$479f936cd1f56903e36340dc7b65f047f7946daa3d0605c7e57603b21c138d29bf66910ca2865dd4a5af02a9372cd307a164acd9352f7c45c49ec6313381b191",
            role="admin",
            display_name="Alexa",
        ),
        User(
            username="marta",
            password_hash="scrypt:32768:8:1$7biPDc4MyI51T5iG$c599a4ff813528c7d003d5cb6637eeb0752beb3e028f585a0cb9435ef105e35d91cfa412aafd21bb8dd7e883957285d8112718d0b29c1e531a4c7583441990a3",
            role="consultant",
            display_name="Marta",
        ),
        User(
            username="tomasz",
            password_hash="scrypt:32768:8:1$uZqfRAdzU4uLfsTy$c4337d74d24f78a815f79fdcb0622de39dfd936e3b4482954634867d6544564a003ecf84ffabe8d42055bfa618def868bccd922d48ab275fd07b0be0b193025b",
            role="consultant",
            display_name="Tomasz",
        ),
    ]
    db.session.add_all(users)
    db.session.flush()


def _seed_core_demo_data():
    marta = User.query.filter_by(username="marta").one()
    tomasz = User.query.filter_by(username="tomasz").one()

    gbs = University(
        name="Global Business School (GBS)",
        partnership_type="Direct contract",
        contact_person="Sarah Johnson",
        contact_email="partners@gbs.ac.uk",
        contact_phone="+44 20 7000 0000",
        application_portal_url="https://apply.gbs.ac.uk",
        status="Active",
    )
    db.session.add(gbs)
    db.session.flush()

    greenford = Campus(
        university=gbs, name="London Greenford", city="London",
        address="Greenford Park, 100 Oldfield Lane North", postcode="UB6 0FD",
        nearest_station="Greenford (Central line)", study_modes="Campus, Hybrid",
    )
    birmingham = Campus(
        university=gbs, name="Birmingham", city="Birmingham",
        address="10 Colmore Row", postcode="B3 2QD",
        nearest_station="Birmingham Snow Hill", study_modes="Campus",
    )
    manchester = Campus(
        university=gbs, name="Manchester", city="Manchester",
        address="1 Portland Street", postcode="M1 3BE",
        nearest_station="Manchester Piccadilly", study_modes="Campus, Hybrid",
    )
    leeds = Campus(
        university=gbs, name="Leeds", city="Leeds",
        address="Wellington Place", postcode="LS1 4AP",
        nearest_station="Leeds", study_modes="Campus",
    )
    online = Campus(
        university=gbs, name="Online", city=None,
        study_modes="Online",
    )
    db.session.add_all([greenford, birmingham, manchester, leeds, online])
    db.session.flush()

    courses = [
        Course(
            university=gbs, campus=greenford, name="Business Management",
            level="Bachelor", category="Business", duration="3 lata",
            intakes="September, January", study_mode="Campus",
        ),
        Course(
            university=gbs, campus=leeds, name="Business Management",
            level="Top-Up", category="Business", duration="1 rok",
            intakes="September", study_mode="Campus",
        ),
        Course(
            university=gbs, campus=birmingham, name="Health and Social Care",
            level="HND", category="Healthcare", duration="2 lata",
            intakes="September, January, April", study_mode="Campus",
        ),
        Course(
            university=gbs, campus=manchester, name="Computing",
            level="Bachelor", category="Computing", duration="3 lata",
            intakes="September, January", study_mode="Hybrid",
        ),
        Course(
            university=gbs, campus=greenford, name="Accounting and Finance",
            level="CertHE", category="Accounting", duration="1 rok",
            intakes="September, January", study_mode="Campus",
        ),
        Course(
            university=gbs, campus=online, name="MBA",
            level="Master", category="Business", duration="18 miesięcy",
            intakes="September, January, April, June", study_mode="Online",
        ),
    ]
    db.session.add_all(courses)
    db.session.flush()

    # 12 studentów: 6 przypisanych do Marty, 6 do Tomasza; po jednej aplikacji
    # na studenta, statusy rozłożone tak, żeby pipeline miał widoczne dane.
    student_specs = [
        # (imię i nazwisko, konsultant, kurs, status aplikacji, intake)
        ("Jan Kowalski", marta, courses[0], "Draft", "September 2026"),
        ("Anna Nowak", marta, courses[0], "Submitted", "September 2026"),
        ("Piotr Zieliński", marta, courses[2], "Interview booked", "September 2026"),
        ("Maria Wiśniewska", marta, courses[3], "Conditional offer", "January 2027"),
        ("Krzysztof Wójcik", marta, courses[5], "Enrolled", "September 2026"),
        ("Magdalena Kamińska", marta, courses[4], "Missing documents", "January 2027"),
        ("Michał Lewandowski", tomasz, courses[1], "Rejected", "September 2026"),
        ("Agnieszka Włodarczyk", tomasz, courses[2], "Under review", "September 2026"),
        ("Łukasz Podolski", tomasz, courses[3], "Unconditional offer", "September 2026"),
        ("Barbara Kwarc", tomasz, courses[0], "Withdrawn", "January 2027"),
        ("Paweł Zarzeczny", tomasz, courses[5], "Enrolled", "September 2026"),
        ("Katarzyna Figura", tomasz, courses[4], "Offer accepted", "September 2026"),
    ]
    for full_name, consultant, course, status, intake in student_specs:
        student = Student(full_name=full_name, consultant=consultant)
        db.session.add(student)
        db.session.add(
            Application(
                student=student,
                university=course.university,
                campus=course.campus,
                course=course,
                intake=intake,
                study_mode=course.study_mode,
                status=status,
                application_date=date(2026, 6, 15),
            )
        )

    db.session.add(
        Update(title="Welcome to ZochAI-CRM", content="Welcome to the ZochAI-CRM")
    )
