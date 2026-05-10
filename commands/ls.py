# commands/ls.py

from rich.text import Text

from contracts import CommandOutput
from .registry import command

@command("ls", help="list directory contents", usage="ls [path]")
def cmd_ls(ctx, args):
    path = args.positionals[0] if args.positionals else None

    children = ctx.fs.ls(path)
    items = sorted(children.items(), key=lambda x: (x[1]["type"] == "file", x[0]))

    text = Text()

    for i, (name, child) in enumerate(items):
        if child["type"] == "dir":
            style = ctx.themer.get("dir", "rich")
            display = f"{name}/"
        else:
            style = ctx.themer.get("file", "rich")
            display = name
        if i < len(items) - 1:
            display += "\n"
        text.append(display, style=style)
    
    plain = "\n".join(name for name, _ in items)
    
    return CommandOutput(styled=text, plain=plain)