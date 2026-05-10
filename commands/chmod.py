# commands/chmod.py

from errors import MissingOperand
from .registry import command

@command("chmod", help="change file permissions", usage="chmod <mode> <path>")
def cmd_chmod(ctx, args):
	if len(args.positionals) < 2:
		raise MissingOperand("chmod")
	mode, path = args.positionals[0], args.positionals[1]
	ctx.fs.chmod(path, mode)
	return None