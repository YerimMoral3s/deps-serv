from app.extensions.db import db
from app.models.refresh_token import RefreshToken
from app.extensions.responses import success_response, error_response

def close_session(user_id, refresh_token):
    """
    Delete a user's refresh token to completely close their session.
    Args:
        user_id (int): The ID of the user.
        refresh_token (str): The refresh token to delete.
    Returns:
        Response: JSON response indicating success or failure.
    """
    try:
        token_entry = RefreshToken.query.filter_by(user_id=user_id, token=refresh_token).first()

        if not token_entry:
            return error_response(message="Invalid or expired refresh token", status_code=401)

        # Delete the token from the database
        db.session.delete(token_entry)
        db.session.commit()

        return success_response(
            message="Session closed successfully",
            data={"user_id": user_id, "refresh_token_deleted": True},
            status_code=200
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            message="An error occurred while closing the session",
            errors=[str(e)],
            status_code=500
        )