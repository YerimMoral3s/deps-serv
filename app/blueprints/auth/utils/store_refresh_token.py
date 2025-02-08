from app.models.refresh_token import RefreshToken
from app.extensions.db import db

def store_refresh_token(user_id, token, expires_at):
    """
    Store a refresh token for a user in the database.
    Args:
        user_id (int): The ID of the user.
        token (str): The refresh token.
        expires_in_days (int): The number of days until the token expires (default is 7 days).
    Returns:
        dict: A dictionary with information about the stored token.
    """
    try:
        # Create a new refresh token record
        refresh_token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )

        # Save the refresh token to the database
        db.session.add(refresh_token)
        db.session.commit()

        return {
            "success": True,
            "message": "Refresh token stored successfully",
            "token_id": refresh_token.id,
            "user_id": refresh_token.user_id,
            "expires_at": refresh_token.expires_at.isoformat()
        }

    except Exception as e:
        print(str(e))
        db.session.rollback()
        return {
            "success": False,
            "message": "An error occurred while storing the refresh token",
            "error": str(e)
        }