from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from models import db, Aportacio
from datetime import date, datetime
import segno
import io
import base64
import stripe
import os
from dotenv import load_dotenv


load_dotenv()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

aportacions_bp = Blueprint("aportacions", __name__)

@aportacions_bp.route("/aportacions")
def aportacions():
    """Pàgina informativa sobre aportacions"""
    return render_template("aportacions.html")

@aportacions_bp.route("/fes-aportacio")
def nova_aportacio():
    """Formulari per fer aportacions"""
    today = date.today().strftime('%Y-%m-%d')
    return render_template("nova_aportacio_inici.html", today=today)

@aportacions_bp.route("/processa-aportacio", methods=['POST'])
def processa_aportacio():
    """Processa el formulari d'aportació"""
    quantitat = request.form.get('quantitat')
    metode = request.form.get('metode_pagament')
    periodicitat = request.form.get('periodicitat')
    
    if not quantitat or not metode:
        flash('Selecciona quantitat i mètode', 'error')
        return redirect(url_for('aportacions.nova_aportacio'))
    
    # Crear registre
    aportacio = Aportacio(
        usuari_id=current_user.id if current_user.is_authenticated else None,
        quantitat=float(quantitat),
        metode_pagament=metode,
        estat='pendent',
        pais=request.form.get('pais', 'Espanya'),
        notes=f"Periodicitat: {periodicitat}"
    )
    
    db.session.add(aportacio)
    db.session.commit()
    
    # Redirigir segons mètode
    # Redirigir segons mètode
    if metode == 'Transferència':
        return redirect(url_for('aportacions.confirmacio', id=aportacio.id))
    elif metode == 'Targeta':
        return redirect(url_for('aportacions.checkout_stripe', id=aportacio.id))
    elif metode == 'PayPal':
        flash('PayPal encara no disponible', 'info')
        return redirect(url_for('aportacions.nova_aportacio'))

@aportacions_bp.route("/checkout-stripe/<int:id>")
def checkout_stripe(id):
    """Crea sessió de pagament Stripe"""
    aportacio = Aportacio.query.get_or_404(id)
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'unit_amount': int(float(aportacio.quantitat) * 100),
                    'product_data': {
                        'name': f'Aportació Adabida #{aportacio.id}',
                        'description': 'Donació voluntària'
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('aportacions.pagament_exit', id=aportacio.id, _external=True),
            cancel_url=url_for('aportacions.nova_aportacio', _external=True),
        )
        return redirect(session.url)
    except Exception as e:
        flash(f'Error creant sessió Stripe: {str(e)}', 'error')
        return redirect(url_for('aportacions.nova_aportacio'))

@aportacions_bp.route("/pagament-exit/<int:id>")
def pagament_exit(id):
    """Pàgina confirmació després de pagament Stripe"""
    aportacio = Aportacio.query.get_or_404(id)
    aportacio.estat = 'confirmada'
    db.session.commit()
    return render_template('pagament_exit.html', aportacio=aportacio)

@aportacions_bp.route("/confirmacio/<int:id>")
def confirmacio(id):
    """Mostra dades bancàries i QR per completar l'aportació"""
    aportacio = Aportacio.query.get_or_404(id)
    
    # Generar QR SEPA
    sepa_data = f"BCD\n002\n1\nSCT\n\nAdabida\nES9501821615200201991993\nEUR{aportacio.quantitat}\n\n\nAportació #{aportacio.id}"
    
    qr = segno.make(sepa_data, error='h')
    buffer = io.BytesIO()
    qr.save(buffer, kind='png', scale=6)
    buffer.seek(0)
    qr_base64 = base64.b64encode(buffer.read()).decode()
    
    return render_template('confirmacio_aportacio.html', 
                          aportacio=aportacio,
                          qr_image=qr_base64)