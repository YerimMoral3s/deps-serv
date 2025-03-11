from app.models.Department import Department
from app.extensions.responses import success_response, error_response

def get_department_by_id(department_id):
    try:
        department = Department.query.get(department_id)

        if not department:
            return error_response(message="Department not found", status_code=404)

        # Serialize department manually
        department_data = {
            "id": department.id,
            "building_id": department.building_id,
            "department_type_id": department.department_type_id,
            "status": department.status,
            "created_at": department.created_at.isoformat() if department.created_at else None,
            "updated_at": department.updated_at.isoformat() if department.updated_at else None,
            "department_type": {
                "id": department.department_type.id,
                "bedrooms": department.department_type.bedrooms,
                "bathrooms": department.department_type.bathrooms,
                "base_rent_price": float(department.department_type.base_rent_price) if department.department_type.base_rent_price else None,
                "description": department.department_type.description
            } if department.department_type else None  # Handle missing department_type
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