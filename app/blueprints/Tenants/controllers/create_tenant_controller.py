from app.models.Tenant import Tenant
from app.extensions.db import db
from sqlalchemy.exc import SQLAlchemyError
from app.extensions.responses import success_response, error_response

def create_tenant_controller(first_name, last_name, phone, email):
    # Input validation
    if not all([first_name, last_name, phone]):
        return error_response(message="Missing required fields", status_code=400)

    try:
        tenant = Tenant.query.filter_by(phone=phone).first()

        if (tenant):
            return error_response(message="El numero de telefono ya existe", status_code=401)

        new_tenant = Tenant(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            status="activo"
        )
        db.session.add(new_tenant)
        db.session.commit()

        return success_response(
            data={
                "id": new_tenant.id,
                "first_name": new_tenant.first_name,
                "last_name": new_tenant.last_name,
                "phone": new_tenant.phone,
                "email": new_tenant.email,
                "status": new_tenant.status,
            },
            message="Tenant created successfully",
            status_code=201
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        return error_response(message="Database error", errors=[str(e)], status_code=500)
