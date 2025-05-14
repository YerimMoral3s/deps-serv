from app.models.Lease import Lease
from app.extensions.db import db
from app.extensions.responses import success_response, error_response
from app.models.Department import Department

def get_department_by_tenant_id(tenant_id):
  try:
    lease = Lease.query.filter_by(tenant_id=tenant_id).first()

    if not lease:
        return error_response(message="Failed to fetch departments")
    
    department = Department.query.get(lease.department_id)

    if not department:
      return error_response(message="Failed to fetch departments")
    
    department_data = {
      "id": department.id,
      "status": department.status,
      "bedrooms": department.bedrooms,
      "bathrooms": department.bathrooms,
      "base_rent_price": float(department.base_rent_price) if department.base_rent_price else None,
      "description": department.description,
      "created_at": department.created_at.isoformat() if department.created_at else None,
      "updated_at": department.updated_at.isoformat() if department.updated_at else None,
      "building": {
        "name": department.building.name,
      } if department.building else None
    }

    return success_response(
      data=department_data,
      message="Department retrieved successfully",
      status_code=200
    )
  except Exception as e:
    return error_response(message="Error fetching tenant", errors=[str(e)], status_code=500)
