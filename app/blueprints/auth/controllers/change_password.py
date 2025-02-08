from flask import current_app
from app.models.User import User
from app.extensions.db import db
from app.blueprints.auth.utils.hash import hash_password
from app.blueprints.auth.utils.tokens import generate_tokens
from app.extensions.validators import validate_password
from app.extensions.responses import error_response, success_response

def change_password(user_id, new_password):
    """
    Change a user's password after validating the old password.
    Args:
        user_id (int): The ID of the user requesting the password change.
        new_password (str): The new password to be set.
    Returns:
        Response: JSON response indicating success or failure.
    """
    try:
        if not all([user_id, new_password]):
            return error_response(message="All fields (user_id, old_password, new_password) are required", status_code=400)

        if not validate_password(new_password):
            return error_response(
                message="New password must be at least 8 characters long, include uppercase, lowercase, a digit, and a special character",
                status_code=400
            )

        user = User.query.filter_by(id=user_id).first()
        if not user:
            return error_response(message="User not found", status_code=404)


        hashed_new_password = hash_password(new_password)

        user.password = hashed_new_password
        db.session.commit()

        tokens = generate_tokens(user.id)

        return success_response(
            message="Password changed successfully",
            data={"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"]},
            status_code=200
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            message="An error occurred while changing the password",
            errors=[str(e)],
            status_code=500
        )