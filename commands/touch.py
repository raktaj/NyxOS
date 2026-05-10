# commands/touch.py

from errors import MissingOperand
from .registry import command

@command("touch", help="create empty file", usage="touch <path>")
def cmd_touch(ctx, args):
    if not args.positionals:
        raise MissingOperand("touch")

    ctx.fs.touch(args.positionals[0])