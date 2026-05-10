# commands/neofetch.py

from contracts import CommandOutput
from .registry import command

from rich.text import Text
from rich.columns import Columns

@command("neofetch", help="show system information", usage="neofetch")
def cmd_neofetch(ctx, args):
    logo = f"""[{ctx.themer.get("banner", "rich")}]
███╗   ██╗██╗   ██╗██╗  ██╗ ██████╗ ███████╗
████╗  ██║╚██╗ ██╔╝╚██╗██╔╝██╔═══██╗██╔════╝
██╔██╗ ██║ ╚████╔╝  ╚███╔╝ ██║   ██║███████╗
██║╚██╗██║  ╚██╔╝   ██╔██╗ ██║   ██║╚════██║
██║ ╚████║   ██║   ██╔╝ ██╗╚██████╔╝███████║
╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝[/]
"""

    # Expanded info (but still minimal and controlled)
    info = [
        ("OS", "NyxOS"),
        ("User", ctx.username),
        ("Shell", "nsh"),
        ("Kernel", "nyx-kernel 0.3"),
        ("Theme", "Nyx Magenta"),
        ("FS", "jsonfs"),
    ]

    # Align keys
    max_key = max(len(k) for k, _ in info)
    info_lines = [
        f"[bold]{k.ljust(max_key)}[/]: {v}"
        for k, v in info
    ]

    # Styled (side-by-side layout)
    logo_render = Text.from_markup(logo)
    info_render = Text.from_markup("\n".join(info_lines))
    styled = Columns([logo_render, info_render])

    # Plain (for redirection)
    plain = "\n".join(f"{k}: {v}" for k, v in info)

    return CommandOutput(styled=styled, plain=plain)