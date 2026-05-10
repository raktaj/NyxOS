# commands/exit.py

from errors import ShellExit
from .registry import command

@command("shutdown", "exit", "quit", help="power off NyxOS", usage="exit | quit | shutdown")
def cmd_shutdown(ctx, args):
    raise ShellExit