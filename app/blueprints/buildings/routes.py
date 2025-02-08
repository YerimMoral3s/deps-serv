from flask import Blueprint, request
from app.extensions.require_api_key import require_api_key
from app.blueprints.buildings.controllers.createBuilding import create_building

buildings_bp = Blueprint("buildings", __name__)

@buildings_bp.route('/create-building', methods=['POST'])
@require_api_key
def create():
  data = request.json
  name = data.get('name')
  return create_building( name=name )

    