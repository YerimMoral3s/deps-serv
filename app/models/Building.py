from sqlalchemy.orm import relationship
from app.extensions.db import db
from datetime import datetime

class Building(db.Model):
    __tablename__ = "buildings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    total_units = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    departments = relationship('Department', back_populates='building')
    
    def __repr__(self):
        return f"<Building(id={self.id}, name='{self.name}', total_units={self.total_units})>"