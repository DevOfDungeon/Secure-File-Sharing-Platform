import jwt
from datetime import datetime, timedelta, timezone
def generate_token(user_id, secret_key):
    payload = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + timedelta(hours=1)
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token
def verify_token(token, secret_key):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

if __name__ == "__main__":
    secret_key = "icecream"
    user_id = 123
    token = generate_token(user_id, secret_key)
    print(f"Generated Token: {token}")
    verified_user_id = verify_token(token, secret_key)
    print(f"Verified User ID: {verified_user_id}")