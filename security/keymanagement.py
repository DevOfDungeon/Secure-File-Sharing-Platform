from rsa import generate_keys, encrypt_aes_key, decrypt_aes_key
from encryption import encrypt_data
from cryptography.hazmat.primitives import serialization
import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


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

def derive_key_from_password(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000,
    )
    raw_key = kdf.derive(password.encode())
    return base64.urlsafe_b64encode(raw_key)

def encrypt_private_pem(private_pem: bytes, password: str):
    salt = os.urandom(16)
    key = derive_key_from_password(password, salt)
    encrypted_pem = Fernet(key).encrypt(private_pem)
    return encrypted_pem, salt

def decrypt_private_pem(encrypted_pem: bytes, password: str, salt: bytes):
    key = derive_key_from_password(password, salt)
    return Fernet(key).decrypt(encrypted_pem)