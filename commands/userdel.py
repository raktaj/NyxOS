# commands/userdel.py

from contracts import CommandOutput
from errors import MissingOperand, PermissionDenied, NyxError
from .registry import command


@command("userdel", help="delete a user", usage="userdel <username>")
def cmd_userdel(ctx, args):
	if not args.positionals:
		raise MissingOperand("userdel")
	if ctx.username != "root":
		raise PermissionDenied()

	username = args.positionals[0]

	if username == ctx.username:
		raise NyxError("userdel: cannot delete the current user")

	try:
		ctx.user_store.delete_user(username)
	except (KeyError, RuntimeError) as e:
		raise NyxError(str(e))

	ctx.fs.rm(f"/home/{username}", recurse=True)
	return CommandOutput.text(f"User '{username}' deleted.")