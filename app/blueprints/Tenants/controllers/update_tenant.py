from flask import request
from app.extensions.db import db
from app.models.Tenant import Tenant
from app.extensions.responses import success_response, error_response

def update_tenant(tenant_id, first_name, last_name, email):
    try:
        tenant = Tenant.query.get(tenant_id)

        if not tenant:
            return error_response(message="Tenant not found", status_code=404)

        tenant.first_name = first_name or tenant.first_name
        tenant.last_name = last_name or tenant.last_name
        tenant.email = email or tenant.email

        db.session.commit()

        return success_response(
            data={
                "id": tenant.id,
                "first_name": tenant.first_name,
                "last_name": tenant.last_name,
                "email": tenant.email,
                "phone": tenant.phone,
                "ine_url": tenant.ine_url,
                "status": tenant.status,
            },
            message="Tenant updated successfully",
            status_code=200,
        )

    except Exception as e:
        db.session.rollback()
        return error_response(message="Error updating tenant", errors=[str(e)], status_code=500)
