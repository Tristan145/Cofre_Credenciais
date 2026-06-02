from cryptography.fernet import Fernet
import os

# Load encryption key from environment variable or generate a new one if it doesn't exist
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
if not ENCRYPTION_KEY:
    ENCRYPTION_KEY = Fernet.generate_key()
    os.environ['ENCRYPTION_KEY'] = ENCRYPTION_KEY

cipher_suite = Fernet(ENCRYPTION_KEY)

def encrypt_string(text):
    return cipher_suite.encrypt(text.encode()).decode()

def decrypt_string(encrypted_text):
    return cipher_suite.decrypt(encrypted_text.encode()).decode()