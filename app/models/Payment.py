from app.extensions.db import db
from sqlalchemy.orm import relationship
from datetime import date
from app.models.Lease import Lease

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    lease_id = db.Column(db.Integer, db.ForeignKey('leases.id'), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    payment_date = db.Column(db.Integer, nullable=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(
        db.Enum('pendiente', 'pagado', 'vencido', 'cancelado', name='payment_status_enum'),
        default='pendiente',
        nullable=False
    )
    payment_method = db.Column(
        db.Enum('efectivo', 'transferencia', 'tarjeta', name='payment_method_enum'),
        nullable=True
    )
    type = db.Column(
      db.Enum('rent','deposit', name='payment_type_enum'),
      nullable=True
    )
    reference_number = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(
        db.TIMESTAMP,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    lease = relationship('Lease', back_populates='payments')