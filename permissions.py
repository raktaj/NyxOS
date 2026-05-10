# permissions.py

from errors import PermissionDenied, InvalidPermission

VALID_PERMISSIONS = {"r", "w", "rw", "none"}

class Permission:
	def __init__(self, owner: str, mode: str = "rw"):
		if mode not in VALID_PERMISSIONS:
			raise InvalidPermission(mode)
		self.owner = owner
		self.mode = mode

	@staticmethod
	def from_node(node: dict) -> "Permission":
		return Permission(
			owner=node.get("owner", "root"),
			mode=node.get("mode", "rw")
		)

	def can_read(self, username: str) -> bool:
		if username == "root":
			return True
		return "r" in self.mode and username == self.owner

	def can_write(self, username: str) -> bool:
		if username == "root":
			return True
		return "w" in self.mode and username == self.owner

	def check_read(self, username: str, path: str | None = None):
		if not self.can_read(username):
			raise PermissionDenied(path)

	def check_write(self, username: str, path: str | None = None):
		if not self.can_write(username):
			raise PermissionDenied(path)