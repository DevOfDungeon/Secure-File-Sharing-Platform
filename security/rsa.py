from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from encryption import encrypt_data

def generate_keys():

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096
    )
    public_key = private_key.public_key()
    return private_key, public_key


def encrypt_aes_key(aes_key, public_key):

    mgf=padding.MGF1(algorithm=hashes.SHA256())
    algo=hashes.SHA256()
    
    ct = public_key.encrypt(aes_key, padding.OAEP(mgf, algo, label=None))
    return ct

def decrypt_aes_key(ct, pvt_key):
    mgf=padding.MGF1(algorithm=hashes.SHA256())
    algo=hashes.SHA256()
    
    aes_key = pvt_key.decrypt(ct, padding.OAEP(mgf, algo, label=None))
    return aes_key


if __name__ == "__main__":
    # Generate keys
    private_key, public_key = generate_keys()

    # AES key from encryption.py
    
    aes_key, encrypted_data = encrypt_data("example.txt")

    # Encrypt the AES key with RSA
    encrypted_aes_key = encrypt_aes_key(aes_key, public_key)

    # Decrypt it back
    decrypted_aes_key = decrypt_aes_key(encrypted_aes_key, private_key)

    # Verify they match
    print("Original AES Key:", aes_key)
    print("Decrypted AES Key:", decrypted_aes_key)
    print("Keys match:", aes_key == decrypted_aes_key)
