from sqlalchemy.orm import relationship
from app.extensions.db import db

class Lease(db.Model):
    __tablename__ = 'leases'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    type = db.Column(db.Enum('prueba', 'regular', name='lease_type_enum'), nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=False)
    payment_day = db.Column(db.Integer, nullable=False)
    monthly_rent = db.Column(db.Numeric(10, 2), nullable=False)
    upfront_payment = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum('activo', 'finalizado', 'renovado', name='lease_status_enum'), default='activo', nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    tenant = relationship('Tenant', back_populates='leases')
    department = relationship('Department', back_populates='leases')
    payments = db.relationship('Payment', back_populates='lease', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Lease(id={self.id}, tenant_id={self.tenant_id}, department_id={self.department_id})>"