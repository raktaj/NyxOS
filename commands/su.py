# commands/su.py

from errors import SwitchUser, AuthenticationError, NyxError
from auth import verify_password
from .registry import command
import getpass

@command("su", help="switch user", usage="su [username]")
def cmd_su(ctx, args):
	target = args.positionals[0] if args.positionals else "root"

	try:
		user = ctx.user_store.get(target)
	except KeyError:
		raise NyxError(f"su: unknown user: {target}")

	# root can switch to anyone without a password
	if ctx.username != "root":
		password = getpass.getpass(f"Password for {target}: ")
		if not verify_password(password, user["salt"], user["hash"]):
			raise AuthenticationError()

	raise SwitchUser(target)