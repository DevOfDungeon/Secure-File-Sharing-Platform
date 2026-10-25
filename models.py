from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    public_key = db.Column(db.Text, nullable=False)
    encrypted_private_key = db.Column(db.LargeBinary, nullable=False)

    
    pbkdf2_salt = db.Column(db.LargeBinary, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class File(db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    filename = db.Column(db.String(255), nullable=False)
    storage_path = db.Column(db.Text, nullable=False)
    nonce = db.Column(db.LargeBinary, nullable=False)
    sha256_hash = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class FileKey(db.Model):
    __tablename__ = "file_keys"

    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(
        db.Integer,
        db.ForeignKey("files.id"),
        nullable=False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    wrapped_key = db.Column(db.LargeBinary, nullable=False)
    role = db.Column(db.String(50), nullable=False)

    __table_args__ = (
        db.UniqueConstraint(
            "file_id",
            "user_id",
            name="uq_file_user"
        ),
    )


class AuditLog(db.Model):
    __tablename__ = "audit_log"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    file_id = db.Column(
        db.Integer,
        db.ForeignKey("files.id"),
        nullable=False
    )
    action = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)