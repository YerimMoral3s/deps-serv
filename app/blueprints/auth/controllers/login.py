from flask import current_app
from app.models.User import User
from app.extensions.responses import success_response, error_response
from app.blueprints.auth.utils.hash import verify_password
from app.blueprints.auth.utils.tokens import generate_tokens
from app.extensions.validators import validate_email
from app.blueprints.auth.utils.store_refresh_token import store_refresh_token


def login_user(email, password):
    """
    Authenticate a user and generate JWT tokens.
    Args:
        email (str): The user's email address.
        password (str): The user's raw password.
    Returns:
        Response: JSON response indicating success or failure.
    """
    try:
        # Validate input fields
        if not email or not password:
            return error_response(message="Email and password are required", status_code=400)
        
        # Validate email format
        if not validate_email(email):
            return error_response(message="Invalid email format", status_code=400)

        # Find user by email
        user = User.query.filter_by(email=email).first()
        if not user:
            return error_response(message="Invalid email or password", status_code=401)

        # Verify the password
        if not verify_password(password, user.password):
            return error_response(message="Invalid email or password", status_code=401)

        # Generate tokens
        tokens = generate_tokens(user.id)
        store_refresh_token(user.id, tokens["refresh_token"], tokens["refresh_exp"])

        # Serialize user data for the response
        user_data = {
            "id": user.id,
            "email": user.email,
        }

        # Return success response
        return success_response(
            message="Login successful",
            data={
                "user": user_data,
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"]
            },
            status_code=200
        )

    except Exception as e:
        return error_response(
            message="An error occurred during login",
            errors=[str(e)],
            status_code=500
        )