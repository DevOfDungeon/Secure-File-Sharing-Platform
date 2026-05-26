import bcrypt
import hashlib as hlib
def hash_password(password):
    # Generate a salt
    salt = bcrypt.gensalt()
    
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hashed_password

def verify_password(password, hashed_password):
    # Verify the password against the hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def sha256(file):
    with open(file, "rb") as f:
        file_content = f.read()
    return hlib.sha256(file_content).hexdigest()

if __name__ == "__main__":
    
    password = "123456"
    hashed = hash_password(password)
    print(f"Hashed password: {hashed}")
    
    file_hash = sha256("example.txt")
    print(f"SHA256 hash of file: {file_hash}")

    is_valid = verify_password(password, hashed)
    print(f"Password is valid: {is_valid}")
    
    
    is_valid_wrong = verify_password("wrong_password", hashed)
    print(f"Wrong password is valid: {is_valid_wrong}")