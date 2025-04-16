from flask import Blueprint, request
from app.extensions.require_api_key import require_api_key
from app.extensions.require_access_token import require_access_token
from .controllers.login import login_user
from .controllers.sign_in import sign_in
from .controllers.close_session import close_session
from .controllers.refresh_credentials import refresh_credentials
from .controllers.change_password import change_password
from app.extensions.responses import error_response

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/login', methods=['POST'])
@require_api_key
def login():
    data = request.json
    return login_user(
        email=data.get('email'),
        password=data.get('password')
    )

@auth_bp.route('/logout', methods=['POST'])
@require_api_key
def logout():
    data = request.json
    user_id = data.get('id')
    refresh_token = data.get('refresh_token')
    
    return close_session(user_id, refresh_token)

@auth_bp.route('/refresh', methods=['POST'])
@require_api_key
def refresh():
    data = request.json
    refresh_token = data.get('refresh_token')

    if not refresh_token:
        return error_response(message="Refresh token is required", status_code=400)

    return refresh_credentials(refresh_token)

@auth_bp.route("/sign-in", methods=["POST"])
@require_api_key
def sign_in_():
    data = request.json
    return sign_in(
        email=data.get('email'),
        password=data.get('password'),
    )

@auth_bp.route('/change_password', methods=['POST'])
@require_api_key
def change_password_():
    data = request.json
    return change_password(        
        user_id=data.get('id'),
        new_password=data.get('new_password')
    )


@auth_bp.route('/test', methods=['GET'])
@require_api_key
@require_access_token
def test():
    print("H")
    return "sd"

