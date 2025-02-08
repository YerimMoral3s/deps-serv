from flask import current_app
import jwt
import uuid
from datetime import datetime, timezone, timedelta

def generate_tokens(user_id):
    """
    Generate a JWT access token and a refresh token for a given user_id.
    Args:
        user_id (int): The ID of the user.
    Returns:
        dict: A dictionary containing the access token and refresh token.
    """
    
    # Load configuration
    jwt_secret = current_app.config['JWT_SECRET_KEY']
    refresh_secret = current_app.config['REFRESH_SECRET_KEY']
    jwt_algorithm = current_app.config['JWT_ALGORITHM']
    access_token_expiry = current_app.config['JWT_ACCESS_TOKEN_EXPIRES_MINUTES']
    refresh_token_expiry = current_app.config['JWT_REFRESH_TOKEN_EXPIRES_DAYS']

    # Current timestamp
    now = datetime.now(timezone.utc)
    refresh_exp = now + timedelta(days=refresh_token_expiry)
    access_exp = now + timedelta(minutes=access_token_expiry)

    # JWT Access Token
    access_token_payload = {
        "user_id": user_id,
        "exp": access_exp,
        "iat": now,
        "jti": str(uuid.uuid4()),
    }

    access_token = jwt.encode(access_token_payload, jwt_secret, algorithm=jwt_algorithm)

    # Refresh Token
    refresh_token_payload = {
        "user_id": user_id,
        "exp": refresh_exp,
        "iat": now,
        "jti": str(uuid.uuid4()),
    }

    refresh_token = jwt.encode(refresh_token_payload, refresh_secret, algorithm=jwt_algorithm)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "refresh_exp": refresh_exp,
        "access_exp": access_exp
    }


def verify_refresh_token(refresh_token, secret):
    """
    Verify the validity of a refresh token.
    Args:
        refresh_token (str): The refresh token to verify.
        secret (str): The secret key for decoding the token.
    Returns:
        dict: The decoded payload if the token is valid.
    Raises:
        jwt.ExpiredSignatureError: If the token is expired.
        jwt.InvalidTokenError: If the token is invalid.
    """
    try:
        payload = jwt.decode(refresh_token, secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Refresh token has expired.")
    except jwt.InvalidTokenError:
        raise Exception("Invalid refresh token.")