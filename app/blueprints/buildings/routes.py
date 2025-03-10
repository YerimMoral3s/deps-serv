from flask import Blueprint, request
from app.extensions.require_api_key import require_api_key
from app.extensions.require_access_token import require_access_token
from app.blueprints.buildings.controllers.createBuilding import create_building
from app.blueprints.buildings.controllers.getBuildings import get_all_buildings
from app.blueprints.buildings.controllers.get_building_by_id import get_building_by_id

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


@buildings_bp.route('/<int:building_id>', methods=['GET'])
def get_building(building_id):
    print(building_id)
    return get_building_by_id(building_id)