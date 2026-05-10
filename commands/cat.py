# commands/cat.py

from errors import MissingOperand
from contracts import CommandOutput
from .registry import command

@command("cat", help="display file contents", usage="cat <file>")
def cmd_cat(ctx, args):
    if not args.positionals:
        raise MissingOperand("cat")

    content = ctx.fs.cat(args.positionals[0])
    return CommandOutput.text(content)