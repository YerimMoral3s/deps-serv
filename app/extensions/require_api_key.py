import jwt
from flask import request, jsonify, current_app
from functools import wraps

def require_api_key(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_token = request.headers.get("x-api-key")
        
        if not auth_token:
            return jsonify({"message": "Missing API Key"}), 401

        try:
            decoded_token = jwt.decode(auth_token, current_app.config["SECRET_KEY"], algorithms=["HS256"])

            api_key = decoded_token.get("API_KEY")

            if not api_key:
                return jsonify({"message": "Invalid API Key structure"}), 403

            if api_key not in current_app.config["API_KEYS"]:
                return jsonify({"message": "Invalid API Key"}), 403

            return f(*args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "API Key expired or invalid"}), 403

        except jwt.InvalidTokenError:
            return jsonify({"message": "API Key expired or invalid"}), 403
            
        except Exception as e:
            current_app.logger.error(f"Unexpected error in API Key validation: {e}")
            return jsonify({"message": "Internal Server Error"}), 500

    return wrapper