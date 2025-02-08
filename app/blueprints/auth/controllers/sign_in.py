from flask import current_app
from app.models.User import User
from app.extensions.db import db
from app.blueprints.auth.utils.hash import hash_password, hash_tel
from app.blueprints.auth.utils.tokens import generate_tokens
from app.blueprints.auth.utils.store_refresh_token import store_refresh_token
from app.extensions.validators import validate_email, validate_password, validate_telephone, validate_latitude, validate_longitude
from app.extensions.responses import error_response, success_response

def sign_in(email, password):
    """
    Register a new user, hash sensitive data, save to the database, and generate JWT tokens.
    Args:
        email (str): The user's email address.
        password (str): The user's raw password.
    Returns:
        Response: JSON response indicating success or failure.
    """
    try:
        # Validate required fields
        if not all([email, password]):
            return error_response(message="All fields (email, password) are required", status_code=400)

        # Validate email format
        if not validate_email(email):
            return error_response(message="Invalid email format", status_code=400)

        # # Validate password strength
        # if not validate_password(password):
        #     return error_response(
        #         message="Password must be at least 8 characters long, include uppercase, lowercase, a digit, and a special character",
        #         status_code=400
        #     )

        # Check if the email already exists
        if User.query.filter_by(email=email).first():
            return error_response(message="Email is already taken", status_code=409)

        # Hash the password and telephone
        hashed_password = hash_password(password)

        # Create the new user
        new_user = User(
            email=email,
            password=hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()

        # Generate tokens
        tokens = generate_tokens(new_user.id)


        # Serialize the user object (excluding sensitive fields)
        user_data = {
            "id": new_user.id,
            "email": new_user.email,
            "created_at": new_user.created_at.isoformat(),
            "updated_at": new_user.updated_at.isoformat(),
        }

        # user_id, token, expires_at
        store_refresh_token(new_user.id, tokens["refresh_token"], tokens["refresh_exp"])

        # Return success response with user data
        return success_response(
            message="User registered successfully",
            data={
                "user": user_data,
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"]
            },
            status_code=201
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            message="An error occurred while registering the user",
            errors=[str(e)],
            status_code=500
        )