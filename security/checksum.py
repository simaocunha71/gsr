"""Módulo responsável por calcular o checksum de uma mensagem
Fonte: https://docs.python.org/3/library/hashlib.html"""

import hashlib

def get_checksum(message, key):
    """Calcula o checksum de uma mensagem concatenada com uma chave usando a função de hash SHA-256"""
    if isinstance(message, bytes):
        message = message.decode('utf-8')  # Converte bytes para string
    if isinstance(key, bytes):
        key = key.decode('utf-8')  # Converte bytes para string
    mensagem = message + key
    hash_object = hashlib.sha256(mensagem.encode())
    checksum = hash_object.hexdigest()
    return checksum