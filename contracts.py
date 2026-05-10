# contracts.py

from dataclasses import dataclass
from typing import Any

from fs import FileSystem
from themer import Themer
from auth import UserStore

@dataclass
class CommandContext:
    fs: FileSystem
    username: str
    themer: Themer
    user_store: UserStore

@dataclass
class CommandOutput:
    styled: Any = None
    plain: str | None = None
    error: bool = False

    @staticmethod
    def text(s: str):
        return CommandOutput(styled=s, plain=s)
