from flask import jsonify

def success_response(data=None, message="Success", status_code=200):
    """
    Generate a standardized success response.
    """
    response = {
        "success": True,
        "message": message,
        "data": data or {}
    }
    return jsonify(response), status_code

def error_response(message="An error occurred", status_code=400, errors=None, error_code=0):
    """
    Generate a standardized error response.
    """
    response = {
        "success": False,
        "message": message,
        "errors": errors or [],
        "error_code": error_code
    }
    return jsonify(response), status_code