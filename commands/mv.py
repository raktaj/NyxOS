# commands/mv.py

from errors import MissingOperand
from .registry import command

@command("cp", help="copy file or directory", usage="cp <src> <dst>")
def cmd_cp(ctx, args):
	if len(args.positionals) < 2:
		raise MissingOperand("cp")
	src, dst = args.positionals[0], args.positionals[1]
	ctx.fs.cp(src, dst)