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
            building.total_units += 1

        db.session.commit()

        return success_response(data=new_department.to_dict(), message="Department created successfully", status_code=201)

    except Exception as e:
        db.session.rollback()
        return error_response(message="An error occurred while creating the department", errors=[str(e)], status_code=500)