# auth.py
import json
import os
import hashlib

USERS_DB = "users.json"

def get_user(username):
    with open(USERS_DB, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data[username]

def hash_password(password: str):
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100_000
    )
    return salt.hex(), key.hex()

def verify_password(password, salt_hex, hash_hex):
    salt = bytes.fromhex(salt_hex)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100_000
    )
    return key.hex() == hash_hex
