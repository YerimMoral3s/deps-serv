from sqlalchemy.orm import relationship
from app.extensions.db import db


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id', ondelete='CASCADE'), nullable=False)
    department_type_id = db.Column(db.Integer, db.ForeignKey('department_types.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.Enum('disponible', 'ocupado', 'mantenimiento', name='status_enum'), default='disponible')
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    building = relationship('Building', back_populates='departments')
    department_type = relationship('DepartmentType', back_populates='departments')
    
    def to_dict(self):
        return {
            'id': self.id,
            'building_id': self.building_id,
            'department_type_id': self.department_type_id,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    def __repr__(self):
        return f"<Department(id={self.id}, building_id={self.building_id}, status={self.status})>"