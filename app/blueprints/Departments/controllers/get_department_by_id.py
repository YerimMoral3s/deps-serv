from app.models.Department import Department
from app.extensions.responses import success_response, error_response

def get_department_by_id(department_id):
    try:
        department = Department.query.get(department_id)

        if not department:
            return error_response(message="Department not found", status_code=404)

        return success_response(
            data=department.to_dict(),
            message="Department retrieved successfully",
            status_code=200
        )

    except Exception as e:
        return error_response(
            message="Failed to fetch department",
            errors=[str(e)],
            status_code=500
        )