from sqlalchemy.orm import relationship
from app.extensions.db import db
from datetime import datetime

class DepartmentType(db.Model):
    __tablename__ = "department_types"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    base_rent_price = db.Column(db.Numeric(10, 2), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    departments = relationship('Department', back_populates='department_type')

    def __repr__(self):
        return f"<DepartmentType(id={self.id}, bedrooms={self.bedrooms}, bathrooms={self.bathrooms}, base_rent_price={self.base_rent_price})>"