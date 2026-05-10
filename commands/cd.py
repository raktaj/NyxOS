# commands/cd.py

from contracts import CommandOutput
from .registry import command
from errors import MissingOperand

@command("cd", help="change directory", usage="cd <path>")
def cmd_cd(ctx, args):
    if not args.positionals:
        raise MissingOperand("cd")
    new_path = ctx.fs.cd(args.positionals[0])
    return None