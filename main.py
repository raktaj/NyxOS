# main.py

import sys
import getpass

from rich.panel import Panel
from rich.console import Console
from rich.align import Align

from commands import load_commands
from fs import FileSystem
from storage import JSONStorage, MemoryStorage
from themer import Themer
from auth import UserStore, verify_password
from shell import run_shell
from boot import BootConfig

def boot(console: Console, themer: Themer, hostname: str):
    console.clear()

    banner_text = Align.center(
        f"{hostname}v0.4\nObscura",
        vertical="middle"
    )

    panel = Panel(
        banner_text,
        border_style=themer.rich("banner"),
        expand=False
    )

    console.print(panel, justify="center")

def login(console, themer, user_store):
    username = console.input("Username: ")

    try:
        user = user_store.get(username)
    except KeyError:
        console.print("Unknown user", style=themer.rich("error"))
        sys.exit(1)

    password = getpass.getpass("Password: ")

    if not verify_password(
        password,
        user["salt"],
        user["hash"]
    ):
        console.print("Login failed!", style=themer.rich("error"))
        sys.exit(1)

    console.print("Login successful!", style=themer.rich("success"))
    return username

def main():
    cfg = BootConfig.load()

    console = Console()
    themer = Themer(cfg.theme)
    user_store = UserStore(cfg.users_db)
    storage = MemoryStorage() if cfg.initramfs else JSONStorage(cfg.ramfile)

    boot(console, themer, cfg.hostname)
    commands = load_commands()
    user = login(console, themer, user_store)
    fs = FileSystem(storage, user)
    run_shell(user, fs, themer, commands, user_store)

if __name__ == "__main__":
    main()