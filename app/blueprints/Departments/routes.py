from flask import Blueprint, request
from app.blueprints.Departments.controllers.create_department import create_department
from app.blueprints.Departments.controllers.get_departments import get_departments
from app.blueprints.Departments.controllers.get_department_by_id import get_department_by_id
from app.blueprints.Departments.controllers.post_assign_department import post_assign_department
from app.blueprints.Departments.controllers.get_department_by_tenant_id import get_department_by_tenant_id
from app.extensions.require_api_key import require_api_key
from app.extensions.require_access_token import require_access_token

# Blueprint for departments
department_bp = Blueprint('department', __name__)

@department_bp.route('', methods=['POST'])
@require_api_key
@require_access_token
def create_departments():
    data = request.get_json()
    building_id = data.get('building_id')
    bedrooms = data.get('bedrooms')
    bathrooms = data.get('bathrooms')
    base_rent_price = data.get('base_rent_price')
    description = data.get('description')
    return create_department(building_id, bedrooms, bathrooms, base_rent_price, description)

@department_bp.route('/<int:building_id>', methods=['GET'])
@require_api_key
@require_access_token
def get__departments(building_id):
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    status = request.args.get('status', default=None, type=str)
    return get_departments(building_id, page, per_page, status)

@department_bp.route('/id/<int:department_id>', methods=['GET'])
@require_api_key
@require_access_token
def get_department(department_id):
    return get_department_by_id(department_id)

@department_bp.route('/assign/<int:department_id>/<int:tenant_id>', methods=['GET'])
@require_api_key
@require_access_token
def assign_department(department_id, tenant_id):
    return post_assign_department(department_id, tenant_id)

@department_bp.route('/tenant/<int:tenant_id>', methods=['GET'])
@require_api_key
@require_access_token
def get_department_by_tenant(tenant_id):
    return get_department_by_tenant_id(tenant_id)