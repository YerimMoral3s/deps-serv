from app.extensions.db import db
from sqlalchemy.orm import relationship

class Tenant(db.Model):
    __tablename__ = 'tenants'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    ine_url = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Enum('activo', 'inactivo'), default='activo')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    leases = relationship('Lease', back_populates='tenant')

    def __repr__(self):
        return f"<Tenant(id={self.id}, name={self.first_name} {self.last_name}, email={self.email})>"