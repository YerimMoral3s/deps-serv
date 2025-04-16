from flask import jsonify
from app.extensions.db import db
from app.models.Tenant import Tenant
from app.models.Department import Department


def get_all_tenants():
    tenants = db.session.query(Tenant).all()
    print(tenants)
    tenants_data = []
    for tenant in tenants:
        tenants_data.append({
            'id': tenant.id,
            'first_name': tenant.first_name,
            'last_name': tenant.last_name,
            'phone': tenant.phone,
            'status': tenant.status,
            # 'building': {
            #   'name': tenant.department.building.name,
            # }
        })
    return jsonify(tenants_data), 200