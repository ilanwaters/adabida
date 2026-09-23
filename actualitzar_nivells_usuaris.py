"""
Script per actualitzar usuaris existents amb el sistema de nivells
Executar una sola vegada després de la migració
"""

from app import app, db
from models.usuari import Usuari
from datetime import datetime
from utils.temps import ara_utc

with app.app_context():
    # Obtenir tots els usuaris
    usuaris = Usuari.query.all()
    
    actualitzats = 0
    for usuari in usuaris:
        canvis = False
        
        # Si no té data_registre, posar ara
        if usuari.data_registre is None:
            usuari.data_registre = ara_utc()
            canvis = True
            print(f"✓ Usuari {usuari.nom_login}: data_registre actualitzada")
        
        # Si no té nivell_usuari, calcular-lo
        if usuari.nivell_usuari is None:
            nivell_calculat = usuari.calcular_nivell_usuari()
            usuari.nivell_usuari = nivell_calculat
            canvis = True
            print(f"✓ Usuari {usuari.nom_login}: nivell assignat -> {nivell_calculat}")
        
        if canvis:
            actualitzats += 1
    
    # Guardar tots els canvis
    db.session.commit()
    
    print(f"\n🎉 Procés completat!")
    print(f"📊 Usuaris actualitzats: {actualitzats}/{len(usuaris)}")
    
    # Mostrar resum de nivells
    print(f"\n📈 Distribució de nivells:")
    blaus = Usuari.query.filter_by(nivell_usuari='blau').count()
    grocs = Usuari.query.filter_by(nivell_usuari='groc').count()
    verds = Usuari.query.filter_by(nivell_usuari='verd').count()
    print(f"   🔵 Blaus (novells): {blaus}")
    print(f"   🟡 Grocs (actius): {grocs}")
    print(f"   🟢 Verds (verificats): {verds}")