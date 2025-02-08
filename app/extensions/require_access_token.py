from flask import request, current_app
from functools import wraps
from datetime import datetime
import jwt
from app.extensions.responses import error_response

def require_access_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return error_response(
                message="Missing or invalid Access Token",
                status_code=401,
                errors=["missing_token"],
                error_code=2001
            )

        try:
            token = auth_header.split("Bearer ")[1]

            jwt_secret = current_app.config.get("JWT_SECRET_KEY")
            jwt_algorithm = current_app.config.get("JWT_ALGORITHM")

            if not jwt_secret or not jwt_algorithm:
                return error_response(
                    message="JWT configuration missing",
                    status_code=500,
                    errors=["jwt_config_missing"],
                    error_code=2002
                )

            payload = jwt.decode(token, jwt_secret, algorithms=[jwt_algorithm])

            # Ensure token hasn't expired
            if datetime.utcfromtimestamp(payload["exp"]) < datetime.utcnow():
                return error_response(
                    message="Access Token invalid or expired",
                    status_code=401,
                    errors=["token_expired"],
                    error_code=2003
                )

        except jwt.ExpiredSignatureError:
            return error_response(
                message="Access Token Expired",
                status_code=401,
                errors=["token_expired"],
                error_code=2003
            )

        except jwt.InvalidTokenError:
            return error_response(
                message="Invalid Access Token",
                status_code=403,
                errors=["invalid_token"],
                error_code=2003
            )

        except Exception as e:
            current_app.logger.error(f"Unexpected error in access token validation: {e}")
            return error_response(
                message="Internal Server Error",
                status_code=500,
                errors=[str(e)],
                error_code=2005
            )

        return f(*args, **kwargs)

    return wrapper