# commands/help.py

from contracts import CommandOutput
from .registry import command, registry
from rich.text import Text


@command("help", help="show this help message", usage="help [command]")
def cmd_help(ctx, args):
    text = Text()
    text.append("Available commands:\n")

    # Deduplicate commands (handle aliases)
    unique_cmds = {id(cmd): cmd for cmd in registry.values()}

    # Compute alignment width
    max_len = max(len(", ".join(cmd.names)) for cmd in unique_cmds.values())

    # Sort by primary command name
    for cmd in sorted(unique_cmds.values(), key=lambda c: c.names[0]):
        names = ", ".join(cmd.names)
        desc = cmd.help or ""
        text.append(f"  {names.ljust(max_len)}  {desc}\n")

    return CommandOutput(styled=text, plain=None)