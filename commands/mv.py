# commands/mv.py

from errors import MissingOperand
from .registry import command

@command("mv", help="move or rename file or directory", usage="mv <src> <dst>")
def cmd_mv(ctx, args):
	if len(args.positionals) < 2:
		raise MissingOperand("mv")
	src, dst = args.positionals[0], args.positionals[1]
	ctx.fs.mv(src, dst)