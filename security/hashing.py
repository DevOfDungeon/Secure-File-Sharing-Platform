import bcrypt
def hash_password(password):
    # Generate a salt
    salt = bcrypt.gensalt()
    
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hashed_password
def verify_password(password, hashed_password):
    # Verify the password against the hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
if __name__ == "__main__":
    
    password = "123456"
    hashed = hash_password(password)
    print(f"Hashed password: {hashed}")
    
    
    is_valid = verify_password(password, hashed)
    print(f"Password is valid: {is_valid}")
    
    
    is_valid_wrong = verify_password("wrong_password", hashed)
    print(f"Wrong password is valid: {is_valid_wrong}")