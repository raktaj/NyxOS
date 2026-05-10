# commands/clear.py

from contracts import CommandOutput
from .registry import command

@command("clear", help="clear the screen", usage="clear")
def cmd_clear(ctx, args):
    return CommandOutput(styled="__CLEAR__", plain=None)