# main.py

import sys
import getpass

from rich.panel import Panel
from rich.console import Console
from rich.align import Align

from theme import BANNER, SUCCESS, ERROR
from auth import get_user, verify_password
from shell import run_shell

console = Console()

def boot():
    console.clear()

    banner_text = Align.center(
        "NyxOS v0.2\nUmbra",
        vertical="middle"
    )

    panel = Panel(
        banner_text,
        border_style=BANNER,
        expand=False
    )

    console.print(panel, justify="center")

def login():
    username = console.input("Username: ")

    try:
        user = get_user(username)
    except KeyError:
        console.print("Unknown user", style=ERROR)
        sys.exit(1)

    password = getpass.getpass("Password: ")

    if not verify_password(
        password,
        user["salt"],
        user["hash"]
    ):
        console.print("Login failed!", style=ERROR)
        sys.exit(1)

    console.print("Login successful!", style=SUCCESS)
    return username

def main():
    boot()
    user = login()
    run_shell(user)

if __name__ == "__main__":
    main()