from dataclasses import dataclass
from fs import FileSystem
from rich.console import Console

@dataclass
class CommandContext:
    fs: FileSystem
    console: Console
    username: str