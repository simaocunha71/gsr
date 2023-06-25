"""Módulo que trata da encriptação/desencriptação de strings
Fontes: 
-> https://www.geeksforgeeks.org/how-to-encrypt-and-decrypt-strings-in-python/
-> https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/"""
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import json

def derive_key_from_password(password):
    """Função que deriva uma chave de 32 bytes a partir de uma senha"""
    salt = b'salt_value'  # Valor do salt (pode ser um valor fixo ou gerado aleatoriamente)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    key = kdf.derive(password.encode())
    return key

def encrypt_string(string, password):
    """Função que encripta uma string em Python através de uma senha"""
    key = derive_key_from_password(password)
    fernet_key = base64.urlsafe_b64encode(key)
    fernet = Fernet(fernet_key)
    encMessage = fernet.encrypt(string.encode())
    
    #print("original string:", string)
    #print("encrypted string:", encMessage)
    
    return encMessage

def decrypt_string(string, password):
    """Função que desencripta uma string em Python através de uma senha"""
    key = derive_key_from_password(password)
    fernet_key = base64.urlsafe_b64encode(key)
    fernet = Fernet(fernet_key)
    decMessage = fernet.decrypt(string).decode()
    
    #print("decrypted string:", decMessage)
    return decMessage

def encrypt_file(file_path, password):
    """Função que encripta um ficheiro usando uma password"""
    json_data = {}
    
    encrypted_data = encrypt_string(json.dumps(json_data), password)
    
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

def decrypt_file(file_path, password):
    """Função que desencripta um arquivo usando uma password"""
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    
    decrypted_data = decrypt_string(encrypted_data, password)
    json_data = json.loads(decrypted_data)
    
    with open(file_path, 'w') as file:
        json.dump(json_data, file, indent=4)