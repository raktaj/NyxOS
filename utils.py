# utils.py

from rich.text import Text

def render_command_help(cmd):
    text = Text()

    names = ", ".join(cmd.names)
    text.append(f"{names}\n", style="bold")

    if cmd.help:
        text.append(f"{cmd.help}\n")

    if cmd.usage:
        text.append("\nUsage:\n", style="bold")
        text.append(f"  {cmd.usage}\n")

    return text