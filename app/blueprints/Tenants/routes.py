from flask import Blueprint, request
from app.extensions.require_api_key import require_api_key
from app.extensions.require_access_token import require_access_token
from app.blueprints.Tenants.controllers.getAllTenants import get_all_tenants
from app.blueprints.Tenants.controllers.create_tenant_controller import create_tenant_controller
from app.blueprints.Tenants.controllers.create_tenant_with_contract import create_tenant_with_contract
from app.blueprints.Tenants.controllers.get_tenant_by_id import get_tenant_by_id
from app.blueprints.Tenants.controllers.update_tenant import update_tenant

tenants_bp= Blueprint("Tenants", __name__)

@tenants_bp.route('', methods=['GET'])
@require_api_key
@require_access_token
def get_all_tenants_():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    search = request.args.get("search", "").strip()

    return get_all_tenants(page, per_page, search)



@tenants_bp.route('', methods=['POST'])
@require_api_key
@require_access_token
def create_tenant():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone = data.get('phone')
    email = data.get('email', None)
    # Call your controller logic here to create the tenant
    return create_tenant_controller(first_name, last_name,  phone, email)


@tenants_bp.route('/create-tenant-contract', methods=['POST'])
@require_api_key
@require_access_token
def create_tenant_contract():
    data = request.get_json()
    # tenant info
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone = data.get('phone')
    email = data.get('email', None)
    # department info
    department_id = data.get('department_id')
    lease_type = data.get('type')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    payment_day = data.get('payment_day')
    monthly_rent = data.get('monthly_rent')
    upfront_payment = data.get('upfront_payment')
    

    return create_tenant_with_contract(first_name, last_name, phone, email, department_id, lease_type, start_date, end_date, payment_day, monthly_rent, upfront_payment)

@tenants_bp.route('/<int:tenant_id>', methods=['GET'])
@require_api_key
@require_access_token
def get_tenant_(tenant_id):
    print(tenant_id)
    return get_tenant_by_id(tenant_id)
    

@tenants_bp.route('/<int:tenant_id>', methods=['PUT'])
@require_api_key
@require_access_token
def updateTenant(tenant_id):
    data = request.get_json()
    # tenant info
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email', None)

    return update_tenant(tenant_id, first_name, last_name, email)
    