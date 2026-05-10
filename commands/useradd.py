# commands/useradd.py

from contracts import CommandOutput
from errors import MissingOperand, PermissionDenied, NyxError
from .registry import command
import getpass


@command("useradd", help="create a new user", usage="useradd <username>")
def cmd_useradd(ctx, args):
	if not args.positionals:
		raise MissingOperand("useradd")

	if ctx.username != "root":
		raise PermissionDenied()

	username = args.positionals[0]
	password = getpass.getpass(f"Password for {username}: ")
	confirm = getpass.getpass("Confirm password: ")

	if password != confirm:
		raise NyxError("useradd: passwords do not match")

	try:
		ctx.user_store.create_user(username, password)
	except RuntimeError as e:
		raise NyxError(str(e))
	
	ctx.fs.mkdir(f"/home/{username}")
	return CommandOutput.text(f"User '{username}' created.")