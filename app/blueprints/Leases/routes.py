from flask import Blueprint, request
from app.blueprints.Leases.controllers.get_tenant_Lease_by_id import get_tenant_Lease_by_id
from app.blueprints.Leases.controllers.create_lease import create_lease_controller
from app.blueprints.Leases.controllers.get_payments_tenant_id import get_payments_tenant_id
from app.blueprints.Leases.controllers.updatePaymentStatus import updatePaymentStatus

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

@leases_bp.route('/<int:tenant_id>', methods=['GET'])
@require_api_key
@require_access_token
def getLease(tenant_id):
    return get_tenant_Lease_by_id(tenant_id)


@leases_bp.route('payments/<int:tenant_id>', methods=['GET'])
@require_api_key
@require_access_token
def getPayments(tenant_id):
    return get_payments_tenant_id(tenant_id)


@leases_bp.route('payments/<int:payment_id>/status', methods=['POST'])
@require_api_key
@require_access_token
def update_payment(payment_id):
    body = request.get_json()
    new_status = body.get("status")
    print(new_status)
    return updatePaymentStatus(payment_id, new_status)


