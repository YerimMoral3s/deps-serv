from flask import current_app
from app.models.refresh_token import RefreshToken
from app.extensions.responses import success_response, error_response
from app.blueprints.auth.utils.tokens import generate_tokens, verify_refresh_token
from app.extensions.db import db

def refresh_credentials(refresh_token):
    """
    Refresh user credentials by verifying the refresh token and generating new tokens.
    
    Args:
        refresh_token (str): The refresh token provided by the user.
    
    Returns:
        Response: JSON response with new access and refresh tokens or an error.
    """
    try:
        
        # Verify the refresh token
        refresh_secret = current_app.config.get("REFRESH_SECRET_KEY")
        decoded_refresh = verify_refresh_token(refresh_token, refresh_secret)
        
        if not decoded_refresh:
            return error_response(
                message="Invalid refresh token",
                status_code=401,
                errors=["The provided refresh token is invalid or expired."],
                error_code=1001
            )

        # Check if the refresh token is revoked or expired
        token_entry = RefreshToken.query.filter_by(token=refresh_token).first()

        if not token_entry:
            return error_response(
                message="Revoked or non-existent refresh token",
                status_code=401,
                errors=["The refresh token has been revoked or does not exist."],
                error_code=1002
            )

        # Generate new tokens
        user_id = decoded_refresh.get("user_id")
        tokens = generate_tokens(user_id)

        # Update the stored refresh token
        token_entry.token = tokens["refresh_token"]
        db.session.commit()

        # Return new tokens
        return success_response(
            message="Tokens refreshed successfully",
            data={
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"]
            },
            status_code=200
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            message="An error occurred while refreshing credentials",
            errors=[str(e)],
            status_code=500,
            error_code=1003
        )