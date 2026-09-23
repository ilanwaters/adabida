from app import app
from models import Entrada

with app.app_context():
    print("📋 Columnes de la taula Entrada:")
    for col in Entrada.__table__.columns:
        print(f" - {col.name} ({col.type})")

