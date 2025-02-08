import re

def validate_email(email):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(email_regex, email) is not None

def validate_password(password):
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def validate_telephone(telephone):
    """
    Validate a telephone number.
    - Allows digits, spaces, dashes, parentheses, and leading '+'
    - Ensures the number contains 7 to 15 digits
    Returns True if valid, False otherwise.
    """
    # Regex for a valid telephone number
    tel_regex = r"^\+?[\d\s\-()]{7,15}$"

    # Check format
    if not re.match(tel_regex, telephone):
        return False

    # Count digits only
    digits_only = re.sub(r"[^\d]", "", telephone)
    if len(digits_only) < 7 or len(digits_only) > 15:
        return False

    return True
    
def validate_latitude(latitude):
    """
    Validate a latitude value.
    - Must be a float or integer
    - Must be between -90 and 90
    Returns True if valid, False otherwise.
    """
    try:
        lat = float(latitude)
        return -90 <= lat <= 90
    except (ValueError, TypeError):
        return False

def validate_longitude(longitude):
    """
    Validate a longitude value.
    - Must be a float or integer
    - Must be between -180 and 180
    Returns True if valid, False otherwise.
    """
    try:
        lon = float(longitude)
        return -180 <= lon <= 180
    except (ValueError, TypeError):
        return False