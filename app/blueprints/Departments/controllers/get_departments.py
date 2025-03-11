from flask import request
from sqlalchemy.orm import joinedload
from app.models.Department import Department
from app.extensions.responses import success_response, error_response


def get_departments(building_id, page, per_page):
    try:
        # Query departments with related department_type
        pagination = Department.query.options(
            joinedload(Department.department_type)  # Load department_type efficiently
        ).filter_by(building_id=building_id).paginate(page=page, per_page=per_page, error_out=False)

        # Convert SQLAlchemy objects to dictionaries
        departments = [
            {
                "id": dept.id,
                "building_id": dept.building_id,
                "status": dept.status,
                "created_at": dept.created_at.isoformat() if dept.created_at else None,
                "updated_at": dept.updated_at.isoformat() if dept.updated_at else None,
                "department_type": {
                    "id": dept.department_type.id,
                    "bedrooms": dept.department_type.bedrooms,
                    "bathrooms": dept.department_type.bathrooms,
                    "base_rent_price": float(dept.department_type.base_rent_price) if dept.department_type.base_rent_price else None,
                    "description": dept.department_type.description
                } if dept.department_type else None  # Handle cases where department_type is missing
            }
            for dept in pagination.items
        ]

        pagination_data = {
            "page": pagination.page,
            "per_page": per_page,
            "total_pages": pagination.pages,
            "total_items": pagination.total,
            "has_next": pagination.has_next
        }

        return success_response(
            data={"departments": departments, "pagination": pagination_data},
            message="Departments retrieved successfully",
            status_code=200
        )

    except Exception as e:
        import traceback
        print(traceback.format_exc())  # Print full error traceback for debugging
        return error_response(message="Failed to fetch departments", errors=[str(e)])