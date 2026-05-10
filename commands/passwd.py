# commands/passwd.py

from contracts import CommandOutput
from errors import PermissionDenied, NyxError
from .registry import command
from auth import verify_password
import getpass

@command("passwd", help="change user password", usage="passwd [username]")
def cmd_passwd(ctx, args):
	if args.positionals:
		if ctx.username != "root":
			raise PermissionDenied()
		target = args.positionals[0]
	else:
		target = ctx.username

	try:
		user = ctx.user_store.get(target)
	except KeyError:
		raise NyxError(f"passwd: unknown user: {target}")

	if ctx.username != "root":
		current = getpass.getpass("Current password: ")
		if not verify_password(current, user["salt"], user["hash"]):
			raise NyxError("passwd: incorrect password")

	new_password = getpass.getpass("New password: ")
	confirm = getpass.getpass("Confirm new password: ")

	if new_password != confirm:
		raise NyxError("passwd: passwords do not match")

	ctx.user_store.change_password(target, new_password)
	return CommandOutput.text(f"Password updated for '{target}'.")