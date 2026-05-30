import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt_data(file_path):
    key = AESGCM.generate_key(bit_length=256)
    aad = os.path.basename(file_path).encode('utf-8')
    with open(file_path, "rb") as f:
        data = f.read()
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, data, aad)
    return key, nonce + ct

def decrypt_data(key, encrypted_data, aad):
    nonce = encrypted_data[:12]
    ct = encrypted_data[12:]
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ct, aad.encode('utf-8'))

if __name__ == "__main__":
    file_path = "example.txt"
    key, encrypted_data = encrypt_data(file_path)
    print(f"Encrypted data: {encrypted_data}")

    decrypted_data = decrypt_data(key, encrypted_data, os.path.basename(file_path))
    print(f"Decrypted data: {decrypted_data.decode('utf-8')}")