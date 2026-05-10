# commands/mkdir.py

from contracts import CommandOutput
from .registry import command

@command("mkdir", help="create directory", usage="mkdir <path>")
def cmd_mkdir(ctx, args):
    if not args.positionals:
        return CommandOutput.err("mkdir: missing operand")

    ctx.fs.mkdir(args.positionals[0])
    return None