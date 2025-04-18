from flask import request
from sqlalchemy.orm import joinedload
from app.models.Tenant import Tenant
from app.models.Lease import Lease
from app.models.Department import Department
from app.extensions.responses import success_response, error_response
from sqlalchemy import or_

def get_all_tenants(page, per_page, search):
    try:
        query = Tenant.query.options(joinedload(Tenant.leases).joinedload(Lease.department).joinedload(Department.building)
)
        if search:
            query = query.filter(
                or_(
                    Tenant.first_name.ilike(f"%{search}%"),
                    Tenant.last_name.ilike(f"%{search}%"),
                    Tenant.phone.ilike(f"%{search}%")
                )
            )

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        tenants = [
            {
                "id": tenant.id,
                "first_name": tenant.first_name,
                "last_name": tenant.last_name,
                "phone": tenant.phone,
                "status": tenant.status,
                "building": {
                    "name": tenant.active_lease.department.building.name,
                } if tenant.active_lease and tenant.active_lease.department and tenant.active_lease.department.building else {}
            }
            for tenant in pagination.items
        ]

        pagination_data = {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total_pages": pagination.pages,
            "total_items": pagination.total,
            "has_next": pagination.has_next
        }

        return success_response(
            data={"tenants": tenants, "pagination": pagination_data},
            message="Tenants retrieved successfully",
            status_code=200
        )

    except Exception as e:
        print(str(e))
        return error_response(message="Error al obtener inquilinos", errors=[str(e)], status_code=500)