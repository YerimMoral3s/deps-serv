from app.models.Lease import Lease
from app.extensions.db import db
from app.extensions.responses import success_response, error_response
from sqlalchemy.exc import SQLAlchemyError
from app.models.Department import Department

def create_lease_controller(
    tenant_id: int,
    department_id: int,
    lease_type: str,
    start_date: str,
    end_date: str,
    payment_day: int,
    monthly_rent: float,
):
    try:
        department = Department.query.get(department_id)
        
        if not department:
            return error_response(message="Department not found", status_code=404)

        if department.status == "ocupado":
            return error_response(message="El departamento ya está ocupado, selecciona otro", status_code=409)


        department.tenant_id = tenant_id
        department.status = "ocupado"

        new_lease = Lease(
            tenant_id=tenant_id,
            department_id=department_id,
            type=lease_type,
            start_date=start_date,
            end_date=end_date,
            payment_day=payment_day,
            monthly_rent=monthly_rent,
        )

        db.session.add(new_lease)
        db.session.commit()

        return success_response(
            message="Contrato creado correctamente",
            data={
                "id": new_lease.id,
                "tenant_id": new_lease.tenant_id,
                "department_id": new_lease.department_id,
                "department": department.building_id
            },
            status_code=201,
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        print(str(e))
        return error_response(
            message="Error al crear el contrato",
            errors=[str(e)],
            status_code=500,
        )