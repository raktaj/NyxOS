# commands/neofetch.py

from rich.text import Text
from rich.columns import Columns
from rich.padding import Padding

from shutil import get_terminal_size

from contracts import CommandOutput
from .registry import command


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

    info = [
        ("OS",     "NyxOS"),
        ("User",   ctx.username),
        ("Shell",  "nsh"),
        ("Kernel", "nyx-kernel 0.4"),
        ("Theme",  "Nyx Magenta"),
        ("FS",     "jsonfs"),
    ]

    max_key = max(len(k) for k, _ in info)
    info_lines = "\n".join(
        f"[bold]{k.ljust(max_key)}[/]  {v}"
        for k, v in info
    )

    # pad info vertically to center it against the 6-line logo
    logo_lines = 6
    info_line_count = len(info)
    top_pad = (logo_lines - info_line_count) // 2

    logo_render = Text.from_markup(logo)
    info_render = Padding(
        Text.from_markup(info_lines),
        (top_pad, 0, 0, 4)
    )

    term_width = get_terminal_size().columns
    logo_width = 46

    if term_width < logo_width + 30:
        styled = Text.from_markup(logo + "\n" + info_lines)
    else:
        styled = Columns([logo_render, info_render])

    plain = "\n".join(f"{k}: {v}" for k, v in info)
    return CommandOutput(styled=styled, plain=plain)