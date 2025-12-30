from app import app, db
from models.categoria import Categoria

categories = [
    {'nom': 'Política', 'icona': '🗳️', 'ordre': 1},
    {'nom': 'Conflictes', 'icona': '⚔️', 'ordre': 2},
    {'nom': 'Cultura', 'icona': '🎨', 'ordre': 3},
    {'nom': 'Societat', 'icona': '👥', 'ordre': 4},
    {'nom': 'Economia', 'icona': '💰', 'ordre': 5},
    {'nom': 'Ciència', 'icona': '🔬', 'ordre': 6},
    {'nom': 'Esports', 'icona': '⚽', 'ordre': 7},
    {'nom': 'Arts', 'icona': '🎭', 'ordre': 8},
    {'nom': 'Tecnologia', 'icona': '💻', 'ordre': 9},
    {'nom': 'Cultura Popular', 'icona': '🎵', 'ordre': 10},
]

with app.app_context():
    for cat in categories:
        existe = Categoria.query.filter_by(nom=cat['nom']).first()
        if not existe:
            nova = Categoria(**cat)
            db.session.add(nova)
    
    db.session.commit()
    print("✅ Categories creades!")

