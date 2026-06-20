# Secure-File-Sharing-Platform

A security-focused file sharing platform built in Python that implements modern cryptographic techniques for protecting files during storage and transfer.


> **Current Status**: *Work In Progress (WIP)* : :  Security layer completed, application layer under development.

---

## Overview

This project demonstrates a **hybrid cryptographic design** for secure file handling using:

- Symmetric encryption for performance (AES-256-GCM)
- Asymmetric encryption for key protection (RSA-OAEP)
- Password security (bcrypt)
- Integrity hashing (SHA-256)
- Token-based authentication (JWT)

The goal is to evolve this into a full-stack secure file-sharing platform using Flask and PostgreSQL, following real-world security design principles.

---

## Security Features

### AES-256-GCM Encryption

Files are encrypted using AES in Galois/Counter Mode (GCM), providing:

- Confidentiality of file contents
- Built-in authentication (tamper detection)
- Integrity protection via authentication tag

Each encryption uses:
- A randomly generated 256-bit key
- A unique 96-bit nonce (`os.urandom(12)`)
- Additional Authenticated Data (AAD)

### Additional Authenticated Data (AAD)

The filename is used as AAD:

- Ensures filename integrity
- Detects unauthorized metadata modification
- Does not encrypt filename (only binds it to ciphertext integrity)

### RSA Key Encryption (Hybrid Encryption)

A hybrid encryption scheme is used:

- AES session key is generated per file
- AES key is encrypted using RSA public key
- RSA uses:
  - 4096-bit key size
  - OAEP padding
  - SHA-256 hash function
  - MGF1 mask generation

This enables secure key exchange.

### Password Security (bcrypt)

User passwords are secured using bcrypt:

- Automatic salt generation
- Adaptive hashing cost factor
- Protection against brute-force and rainbow table attacks

### SHA-256 File Hashing

SHA-256 is used to generate file fingerprints:

- Detects file corruption or modification
- Provides external integrity verification (outside AES-GCM)

### JWT Authentication

JWT is used for session authentication:

- Encodes user identity
- Includes expiration time (1 hour)
- Signed using HS256

---

## Cryptographic Workflow

### Encryption Flow

1. Read file from disk
2. Generate random 256-bit AES key
3. Generate 96-bit nonce using `os.urandom(12)`
4. Set filename as AAD
5. Encrypt file using AES-256-GCM
6. Combine nonce + ciphertext output
7. Encrypt AES key using RSA-OAEP public key
8. Store:
   - Encrypted file data
   - Encrypted AES key
   - Nonce (embedded in output)

---

### Decryption Flow

1. Decrypt AES key using RSA private key
2. Extract nonce from encrypted payload
3. Separate ciphertext and authentication tag
4. Decrypt using AES-GCM with AAD
5. Verify integrity automatically via GCM

---
### Project Structure

```text
Secure-File-Sharing-Platform/
│
├── security/
│   ├── encryption.py   # AES-GCM encryption/decryption
│   ├── rsa.py          # RSA key generation + key wrapping
│   ├── hashing.py      # bcrypt + SHA-256 utilities
│   ├── auth.py         # JWT authentication
│   └── example.txt     # Test file
│ 
└── README.md
```
---

Technologies Used
   - Python 3
   - cryptography
   - bcrypt
   - PyJWT
   - AES-256-GCM
   - RSA-4096 (OAEP)
   - SHA-256
..........

## Threat Model
### Threats
   - Network eavesdropping
   - File tampering
   - Unauthorized file access
   - Credential theft
   - Session hijacking

### Security Controls
- AES-GCM authenticated encryption
- RSA-based key encapsulation
- bcrypt password hashing
- JWT authentication with expiration
- Cryptographically secure nonce generation
- SHA-256 file fingerprinting

## Notes
```text
AES-GCM already provides integrity; SHA-256 is used for external verification/fingerprinting

RSA is used only for encrypting AES session keys (not bulk data)

Nonces are randomly generated per encryption to ensure uniqueness

AAD binds filename to ciphertext integrity
```
## Learning Objectives

This project was built to understand:

- Applied cryptography
- Hybrid encryption design
- Secure authentication systems
- Password storage security
- File integrity verification
- Backend security architecture

## Planned Features
```
Flask backend API

PostgreSQL database integration

User authentication system

Secure file upload/download endpoints

Role-based access control

File sharing between users

Audit logging system

Key management system

Docker / Kubernetes deployment

Security testing suite
```