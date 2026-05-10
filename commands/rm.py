# commands/rm.py

from errors import MissingOperand
from parser import ArgumentSpec
from .registry import command

@command(
    "rm",
    help="remove file or directory",
    usage="rm [-r] <path>",
    argspec=ArgumentSpec(flags={"r"})
)
def cmd_rm(ctx, args):
    if not args.positionals:
        raise MissingOperand("rm")

    path = args.positionals[0]
    recursive = args.flags.get("r", False)

    ctx.fs.rm(path, recurse=recursive)