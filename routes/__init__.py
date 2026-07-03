from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.student_routes import students_bp
from routes.university_routes import universities_bp
from routes.updates_routes import updates_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(universities_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(updates_bp)
