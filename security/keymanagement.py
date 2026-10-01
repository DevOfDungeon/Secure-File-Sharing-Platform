from rsa import generate_keys, encrypt_aes_key, decrypt_aes_key
from encryption import encrypt_data
from cryptography.hazmat.primitives import serialization


def private_key_to_pem(private_key):
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


def pem_to_private_key(pem_bytes):
    return serialization.load_pem_private_key(
        pem_bytes,
        password=None,
    )

def public_key_to_pem(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def pem_to_public_key(pem_bytes):
    return serialization.load_pem_public_key(
        pem_bytes,
    )

