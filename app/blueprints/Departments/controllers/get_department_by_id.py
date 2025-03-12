from app.models.Department import Department
from app.extensions.responses import success_response, error_response

def get_department_by_id(department_id):
    try:
        department = Department.query.get(department_id)

        if not department:
            return error_response(message="Department not found", status_code=404)

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
        return error_response(
            message="Failed to fetch department",
            errors=[str(e)],
            status_code=500
        )