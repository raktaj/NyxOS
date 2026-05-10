# auth.py

import json
import os
import hashlib
import hmac


class UserStore:
    def __init__(self, path: str = "users.json"):
        self._path = path
        self._users: dict = self._load()

    def _load(self) -> dict:
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise RuntimeError("User database missing")

    def get(self, username: str) -> dict:
        try:
            return self._users[username]
        except KeyError:
            raise KeyError(f"Unknown user: {username}")

    def reload(self):
        self._users = self._load()

    def create_user(self, username: str, password: str):
        if username in self._users:
            raise RuntimeError(f"User already exists: {username}")
        salt, key = hash_password(password)
        self._users[username] = {"salt": salt, "hash": key}
        self._persist()

    def change_password(self, username: str, new_password: str):
        if username not in self._users:
            raise KeyError(f"Unknown user: {username}")
        salt, key = hash_password(new_password)
        self._users[username]["salt"] = salt
        self._users[username]["hash"] = key
        self._persist()

    def _persist(self):
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(self._users, f, indent="\t")

# to be used by: useradd (planned)
def hash_password(password: str) -> tuple[str, str]:
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100_000
    )
    return salt.hex(), key.hex()


def verify_password(password: str, salt_hex: str, hash_hex: str) -> bool:
    salt = bytes.fromhex(salt_hex)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100_000
    )
    return hmac.compare_digest(key.hex(), hash_hex)

