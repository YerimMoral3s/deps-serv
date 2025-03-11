from app.extensions.db import db
from app.models.Department import Department
from app.models.Building import Building
from app.extensions.responses import success_response, error_response

def create_department(building_id, department_type_id):
    if not building_id or not department_type_id:
        return error_response("Missing required fields", 400)

    try:
        # Create the department
        new_department = Department(
            building_id=building_id,
            department_type_id=department_type_id,
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
            # "building_id": new_department.building_id,
            # "department_type_id": new_department.department_type_id,
            # "status": new_department.status,
            # "created_at": new_department.created_at.isoformat() if new_department.created_at else None,
            # "updated_at": new_department.updated_at.isoformat() if new_department.updated_at else None
        }

        return success_response(data=department_data, message="Department created successfully", status_code=201)

    except Exception as e:
        db.session.rollback()
        return error_response(message="An error occurred while creating the department", errors=[str(e)], status_code=500)