import os

from flask import Flask

from models import ROLE_LABELS, db
from routes import register_blueprints
from seed import init_db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-insecure-key-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///crm.db"  # instance/crm.db

db.init_app(app)
register_blueprints(app)
init_db(app)

# Etykiety ról dostępne we wszystkich szablonach.
app.jinja_env.globals["ROLE_LABELS"] = ROLE_LABELS


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("--- ZochAI-CRM uruchomiony pomyślnie! ---")
    print(f"Otwórz w przeglądarce: http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
