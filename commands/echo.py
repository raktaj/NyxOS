# commands/echo.py

from contracts import CommandOutput
from .registry import command

@command("echo", help="print text", usage="echo <text>")
def cmd_echo(ctx, args):
    return CommandOutput.text(" ".join(args.positionals))