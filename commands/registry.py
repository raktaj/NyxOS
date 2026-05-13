# commands/registry.py

from dataclasses import dataclass
from typing import Callable
from parser import ArgumentSpec


@dataclass
class Command:
    names: list[str]
    handler: Callable
    help: str
    usage: str | None = None
    argspec: ArgumentSpec | None = None
    path: str | None = None


class CommandRegistry:
    def __init__(self):
        self._commands: dict[str, Command] = {}

    def register(self, cmd: Command):
        for name in cmd.names:
            if name in self._commands:
                raise RuntimeError(f"Duplicate command: {name}")
            self._commands[name] = cmd

    def get(self, name: str) -> Command | None:
        return self._commands.get(name)

    def all(self) -> dict[str, Command]:
        return self._commands

    def __contains__(self, name: str) -> bool:
        return name in self._commands

    def __iter__(self):
        return iter(self._commands)

    def items(self):
        return self._commands.items()

    def values(self):
        return self._commands.values()


registry = CommandRegistry()


def command(*names, help: str = "", usage: str | None = None, argspec: ArgumentSpec | None = None):
    def decorator(func):
        cmd = Command(
            names=list(names),
            handler=func,
            help=help,
            usage=usage,
            argspec=argspec,
            path=f"/bin/{names[0]}"
        )
        registry.register(cmd)
        return func
    return decorator