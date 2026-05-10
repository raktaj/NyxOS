# commands/whoami.py

from contracts import CommandOutput
from .registry import command

@command("whoami", help="show current user", usage="whoami")
def cmd_whoami(ctx, args):
    return CommandOutput.text(ctx.username)