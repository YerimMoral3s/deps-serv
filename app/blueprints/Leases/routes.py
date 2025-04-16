from flask import Blueprint, request
from app.blueprints.Leases.controllers.create_lease import create_lease_controller

from app.extensions.require_api_key import require_api_key
from app.extensions.require_access_token import require_access_token

# Blueprint for leases
leases_bp = Blueprint('leases', __name__)

@leases_bp.route('', methods=['POST'])
@require_api_key
@require_access_token
def create_lease():
    data = request.get_json()
    tenant_id = data.get('tenant_id')
    department_id = data.get('department_id')
    lease_type = data.get('type')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    payment_day = data.get('payment_day')
    monthly_rent = data.get('monthly_rent')

    return create_lease_controller(
        tenant_id,
        department_id,
        lease_type,
        start_date,
        end_date,
        payment_day,
        monthly_rent
    )

