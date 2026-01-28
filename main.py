# main.py
import os
import sys
import getpass

from theme import BANNER, SUCCESS, ERROR
from auth import get_user, verify_password
from shell import run_shell

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def boot():
    clear_screen()
    print(f"{BANNER}NyxOS v0.1")

def login():
    username = input("Username: ")

    try:
        user = get_user(username)
    except KeyError:
        print(f"{ERROR}Unknown user")
        sys.exit(1)

    password = getpass.getpass("Password: ")

    if not verify_password(
        password,
        user["salt"],
        user["hash"]
    ):
        print(f"{ERROR}Login failed!")
        sys.exit(1)

    print(f"{SUCCESS}Login successful!")
    return username

def main():
    boot()
    user = login()
    run_shell(user)

if __name__ == "__main__":
    main()
