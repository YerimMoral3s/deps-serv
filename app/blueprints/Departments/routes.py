from flask import Blueprint, request
from app.blueprints.Departments.controllers.create_department import create_department
from app.extensions.require_api_key import require_api_key
from app.extensions.require_access_token import require_access_token

# Blueprint for departments
department_bp = Blueprint('department', __name__)

@department_bp.route('/', methods=['POST'])
@require_api_key
@require_access_token
def create_departments():
    data = request.get_json()
    building_id = data.get('building_id')
    department_type_id = data.get('department_type_id')
    return create_department(building_id, department_type_id)





