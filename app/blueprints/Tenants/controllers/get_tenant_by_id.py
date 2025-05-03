from app.extensions.db import db
from app.models.Tenant import Tenant
from app.models.Department import Department
from app.extensions.responses import success_response, error_response

def get_tenant_by_id(tenant_id):
    try:
        tenant = Tenant.query.get(tenant_id)

        if not tenant:
            return error_response(message="Tenant not found", status_code=404)

        tenant_data = {
            "id": tenant.id,
            "first_name": tenant.first_name,
            "last_name": tenant.last_name,
            "phone": tenant.phone,
            "email": tenant.email,
            "status": tenant.status,
            "ine_url": tenant.ine_url,
        }

        return success_response(data=tenant_data, message="Tenant fetched successfully")
    
    except Exception as e:
        return error_response(message="Error fetching tenant", errors=[str(e)], status_code=500)