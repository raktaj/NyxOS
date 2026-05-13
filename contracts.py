# contracts.py

from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from commands.registry import CommandRegistry
    from fs import FileSystem
    from themer import Themer
    from auth import UserStore


@dataclass
class CommandContext:
    fs: FileSystem
    username: str
    themer: Themer
    user_store: UserStore
    commands: CommandRegistry


@dataclass
class CommandOutput:
    styled: Any = None
    plain: str | None = None

    @staticmethod
    def text(s: str):
        return CommandOutput(styled=s, plain=s)
