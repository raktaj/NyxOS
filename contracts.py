# contracts.py

from dataclasses import dataclass
from typing import Any

from fs import FileSystem

@dataclass
class CommandContext:
    fs: FileSystem
    username: str

@dataclass
class CommandOutput:
    styled: Any = None
    plain: str | None = None
    error: bool = False

    @staticmethod
    def text(s: str):
        return CommandOutput(styled=s, plain=s)

    @staticmethod
    def err(msg: str):
        return CommandOutput(styled=msg, plain=None, error=True)