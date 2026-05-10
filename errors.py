# errors.py

class ShellExit(Exception):
	pass


class SwitchUser(Exception):
	def __init__(self, username: str):
		self.username = username
		super().__init__(username)


class NyxError(Exception):
	pass


class MissingOperand(NyxError):
	def __init__(self, cmd):
		super().__init__(f"{cmd}: missing operand")


class NoSuchFile(NyxError):
	def __init__(self, path=None):
		msg = "no such file or directory"
		if path:
			msg += f": {path}"
		super().__init__(msg)


class NotADirectory(NyxError):
	def __init__(self, path=None):
		msg = "not a directory"
		if path:
			msg += f": {path}"
		super().__init__(msg)


class IsADirectory(NyxError):
	def __init__(self, path=None):
		msg = "is a directory"
		if path:
			msg += f": {path}"
		super().__init__(msg)


class DirectoryNotEmpty(NyxError):
	def __init__(self, path=None):
		msg = "directory not empty"
		if path:
			msg += f": {path}"
		super().__init__(msg)

class FileExists(NyxError):
	def __init__(self, path=None):
		msg = "is a file"
		if path:
			msg += f": {path}"
		super().__init__(msg)

class PermissionDenied(NyxError):
	def __init__(self, path=None):
		msg = "permission denied"
		if path:
			msg += f": {path}"
		super().__init__(msg)

class InvalidPermission(NyxError):
	def __init__(self, value=None):
		msg = "invalid permission"
		if value:
			msg += f": {value}"
		super().__init__(msg)

class AuthenticationError(NyxError):
	def __init__(self):
		super().__init__("authentication failure")