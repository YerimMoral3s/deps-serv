from sqlalchemy.orm import relationship
from app.extensions.db import db


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.Enum('disponible', 'ocupado', 'mantenimiento', name='status_enum'), default='disponible')
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    base_rent_price = db.Column(db.Numeric(10,2), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    leases = relationship('Lease', back_populates='department')

    building = relationship('Building', back_populates='departments')