"""Módulo responsável por calcular o checksum de uma mensagem
Fonte: https://docs.python.org/3/library/hashlib.html"""

import hashlib

def get_checksum(message, key):
    # Converte a chave para bytes, se necessário
    if isinstance(key, str):
        key = key.encode()

    # Concatena a mensagem e a chave
    mensagem = message + key

    # Calcula o checksum utilizando a função de hash SHA-256
    hash_object = hashlib.sha256(mensagem)
    checksum = hash_object.hexdigest()

    return checksum
 