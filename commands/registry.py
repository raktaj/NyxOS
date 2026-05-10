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

COMMANDS = {}

def command(*names, help: str = "", usage: str | None = None, argspec: ArgumentSpec | None = None):
    def decorator(func):
        cmd = Command(
            names=list(names),
            handler=func,
            help=help,
            usage=usage,
            argspec=argspec
        )

        for name in names:
            if name in COMMANDS:
                raise RuntimeError(f"Duplicate command: {name}")
            COMMANDS[name] = cmd

        return func
    return decorator