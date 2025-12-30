from models import db
from datetime import datetime


class EntradaBlog(db.Model):
    __tablename__ = 'entrades_blog'

    id = db.Column(db.Integer, primary_key=True)
    titol = db.Column(db.String(200), nullable=False)
    contingut = db.Column(db.Text, nullable=False)
    data_creacio = db.Column(db.DateTime, default=datetime.utcnow)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuaris.id'))
    firma = db.Column(db.String(120))