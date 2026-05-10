# storage.py

import json
import copy
from typing import Protocol, runtime_checkable


@runtime_checkable
class StorageProtocol(Protocol):
	def load(self) -> dict: ...
	def save(self, data: dict) -> None: ...


class JSONStorage:
	def __init__(self, path):
		self.path = path

	def load(self):
		try:
			with open(self.path, "r", encoding="utf-8") as f:
				return json.load(f)
		except FileNotFoundError:
			# optional: initialize empty FS
			return {"/": {"type": "dir", "children": {}}}

	def save(self, data):
		with open(self.path, "w", encoding="utf-8") as f:
			json.dump(data, f, indent=2)


class MemoryStorage:
	def __init__(self, initial=None):
		self.data = initial or {"/": {"type": "dir", "children": {}}}

	def load(self):
		return copy.deepcopy(self.data)

	def save(self, data):
		self.data = data