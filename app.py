import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

# imported after db exists to avoid a circular import
from models import User
from security.hashing import hash_password, verify_password
from security.rsa import generate_keys
from security.keymanagement import (
    private_key_to_pem,
    public_key_to_pem,
    encrypt_private_pem,
)
from security.auth import generate_token

JWT_SECRET = os.getenv("JWT_SECRET")

@app.route("/")
def home():
    return "Secure File Sharing Platform is running!"

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or len(password) < 8:
        return jsonify(error="username required, password must be 8+ chars"), 400
    if User.query.filter_by(username=username).first():
        return jsonify(error="username already taken"), 409

    private_key, public_key = generate_keys()
    encrypted_pem, salt = encrypt_private_pem(private_key_to_pem(private_key), password)

    user = User(
        username=username,
        password_hash=hash_password(password).decode(),
        public_key=public_key_to_pem(public_key).decode(),
        encrypted_private_key=encrypted_pem,
        pbkdf2_salt=salt,
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(message="registered", user_id=user.id), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    user = User.query.filter_by(username=username).first()
    if not user or not verify_password(password, user.password_hash.encode()):
        return jsonify(error="invalid credentials"), 401

    return jsonify(token=generate_token(user.id, JWT_SECRET))

if __name__ == "__main__":
    app.run(debug=True)