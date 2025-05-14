from app.extensions.db import db
from app.extensions.responses import success_response, error_response
from app.models.Tenant import Tenant
from app.models.Lease import Lease
from app.models.Department import Department
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from dateutil.relativedelta import relativedelta
from app.models.Payment import Payment
from calendar import monthrange

def create_tenant_with_contract(first_name, last_name, phone, email, department_id, lease_type, start_date, end_date, payment_day, monthly_rent, upfront_payment):
    try:
        with db.session.begin():
            # # Check if department exist
            department = Department.query.get(department_id)
            if not department:
                return error_response("Departamento no encontrado", status_code=404)
            if department.status == "ocupado":
                return error_response("El departamento ya está ocupado", status_code=409)
        
            # Check if tenant exist
            existing = Tenant.query.filter_by(phone=phone).first()
            if existing:
                if existing.status == 'inactivo':
                    existing.status = 'activo'
                    db.session.flush()
                    tenant = existing
                else:
                    return error_response("Ya existe un inquilino con ese teléfono", status_code=409)
            else:
                tenant = Tenant(
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    email=email,
                )
                db.session.add(tenant)
                db.session.flush()

            # create lease
            lease = Lease(
                tenant_id=tenant.id,
                department_id=department_id,
                type=lease_type,
                start_date=start_date,
                end_date=end_date,
                payment_day=payment_day,
                upfront_payment=upfront_payment,
                monthly_rent=monthly_rent,
            )

            db.session.add(lease)
            db.session.flush()

            # create upfront payment if applicable
            if upfront_payment and float(upfront_payment) > 0:
                db.session.add(Payment(
                    lease_id=lease.id,
                    due_date=datetime.strptime(start_date, "%Y-%m-%d").date(),
                    amount=upfront_payment,
                    status="pendiente",
                    type="deposit"
                ))

            # create payments 
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")

            current_due_date = start

            while current_due_date < end:
                last_day = monthrange(current_due_date.year, current_due_date.month)[1]
                safe_day = min(int(payment_day), last_day)
                due_date = current_due_date.replace(day=safe_day)
                db.session.add(Payment(
                    lease_id=lease.id,
                    due_date=due_date.date(),
                    amount=monthly_rent,
                    status="pendiente",
                    payment_date=payment_day,
                    type="rent"
                ))
                current_due_date += relativedelta(months=1)

            # assign department to tenant
            department.tenant_id = tenant.id
            department.status = "ocupado"

            building_id = department.building_id if department else None

        return success_response(
            message="Inquilino registrado correctamente",
            data={
                "tenant_id": tenant.id, 
                "building_id": building_id,
                "department_id": department.id
            },
            status_code=201
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        print(str(e))
        return error_response("Error al crear el inquilino y contrato", errors=[str(e)], status_code=500)
