from app.extensions.db import db
from app.models.Department import Department
from app.models.Building import Building
from app.extensions.responses import success_response, error_response

def create_department(building_id, bedrooms, bathrooms, base_rent_price=None, description=None):
    if not building_id or bedrooms is None or bathrooms is None:
        return error_response("Missing required fields", 400)

    try:
        # Create the department
        new_department = Department(
            building_id=building_id,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            base_rent_price=base_rent_price,
            description=description
        )
        db.session.add(new_department)

        # Update total_units in the building
        building = Building.query.get(building_id)
        if building:
            building.total_units += 1  # Assuming `total_units` is an integer field in `Building`

        db.session.commit()

        # Serialize the department manually
        department_data = {
            "id": new_department.id,
            "building_id": new_department.building_id,
            "bedrooms": new_department.bedrooms,
            "bathrooms": new_department.bathrooms,
            "base_rent_price": float(new_department.base_rent_price) if new_department.base_rent_price else None,
            "description": new_department.description,
            "created_at": new_department.created_at.isoformat() if new_department.created_at else None,
            "updated_at": new_department.updated_at.isoformat() if new_department.updated_at else None
        }

        return success_response(data=department_data, message="Department created successfully", status_code=200)

    except Exception as e:
        db.session.rollback()
        return error_response(message="An error occurred while creating the department", errors=[str(e)], status_code=500)