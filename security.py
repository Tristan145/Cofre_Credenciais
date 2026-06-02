from cryptography.fernet import Fernet
import os

# Tenta carregar a chave das variáveis de ambiente
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')

# Se não existir, gera uma nova chave
if not ENCRYPTION_KEY:
    # generate_key() retorna bytes, usamos .decode() para converter para string
    ENCRYPTION_KEY = Fernet.generate_key().decode()
    os.environ['ENCRYPTION_KEY'] = ENCRYPTION_KEY

# O Fernet exige que a chave seja passada em bytes, então usamos .encode()
cipher_suite = Fernet(ENCRYPTION_KEY.encode())

def encrypt_string(text):
    return cipher_suite.encrypt(text.encode()).decode()

def decrypt_string(encrypted_text):
    return cipher_suite.decrypt(encrypted_text.encode()).decode()