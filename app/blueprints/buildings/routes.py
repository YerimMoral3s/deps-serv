from flask import Blueprint, request
from app.extensions.require_api_key import require_api_key
from app.extensions.require_access_token import require_access_token
from app.blueprints.buildings.controllers.createBuilding import create_building
from app.blueprints.buildings.controllers.getBuildings import get_all_buildings

buildings_bp = Blueprint("buildings", __name__)

@buildings_bp.route('/', methods=['GET'])
@require_api_key
@require_access_token
def get_buildings():
  return get_all_buildings()


@buildings_bp.route('/create-building', methods=['POST'])
@require_api_key
@require_access_token
def create():
  data = request.json
  name = data.get('name')
  return create_building( name=name )
