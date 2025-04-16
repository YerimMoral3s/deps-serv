
from app.models.Department import Department
from app.extensions.responses import success_response, error_response
from app.extensions.db import db

def post_assign_department(department_id, tenant_id):
    department = Department.query.get(department_id)

    if department.status == "ocupado":
        return error_response(message="El departamento ya está ocupado", status_code=409)

    if not department:
        return error_response(message="Department not found", status_code=404)

    department.tenant_id = tenant_id
    department.status = "ocupado"

    db.session.commit()

    return success_response(data={"id": department.id}, message="Department assigned to tenant successfully")