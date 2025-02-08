from flask import Blueprint, request
from app.extensions.require_api_key import require_api_key
from app.extensions.require_access_token import require_access_token
from app.extensions.responses import error_response

buildings_bp = Blueprint("buildings", __name__)

@buildings_bp.route('/test', methods=['GET'])
@require_api_key
def login():
    print("hi")