# commands/rmdir.py

from errors import MissingOperand
from .registry import command

@command("rmdir", help="remove empty directory", usage="rmdir <path>")
def cmd_rmdir(ctx, args):
    if not args.positionals:
        raise MissingOperand("rmdir")

    ctx.fs.rmdir(args.positionals[0])