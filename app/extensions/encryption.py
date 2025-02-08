from cryptography.fernet import Fernet

class EncryptionService:
    def __init__(self, secret_key):
        self.cipher = Fernet(secret_key)

    def encrypt(self, data):
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, token):
        return self.cipher.decrypt(token.encode()).decode()