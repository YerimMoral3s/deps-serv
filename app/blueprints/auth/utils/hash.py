import bcrypt
import hashlib

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def hash_tel(tel):
    """
    Hashes a telephone number using SHA256.
    Returns the hashed telephone number as a hexadecimal string.
    """
    if not tel:
        raise ValueError("Telephone number cannot be empty.")
    
    # Hash the telephone number
    tel_hash = hashlib.sha256(tel.encode('utf-8')).hexdigest()
    return tel_hash