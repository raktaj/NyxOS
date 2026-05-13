# commands/which.py

from contracts import CommandOutput
from errors import MissingOperand, NyxError
from .registry import command


@command("which", help="locate a command", usage="which <name>")
def cmd_which(ctx, args):
    if not args.positionals:
        raise MissingOperand("which")
    name = args.positionals[0]
    cmd = ctx.commands.get(name)
    if not cmd:
        raise NyxError(f"which: {name}: not found")
    return CommandOutput.text(cmd.path)