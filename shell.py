from rich.console import Console
from rich.text import Text

from theme import PROMPT, ERROR, CWD_PARENT, CWD_CURRENT, CWD_SEP
from commands import COMMANDS
from context import CommandContext
from fs import FileSystem
from shell_exceptions import ShellExit

console = Console()
fs = FileSystem()

def format_cwd(path):
    text = Text()
    parts = [p for p in path.split("/") if p]

    if not parts:
        text.append("/", style=CWD_CURRENT)
        return text

    # Parent path
    if len(parts) > 1:
        for part in parts[:-1]:
            text.append("/", style=CWD_SEP)
            text.append(part, style=CWD_PARENT)
        text.append("/", style=CWD_SEP)
    else:
        text.append("/", style=CWD_SEP)

    # Current dir
    text.append(parts[-1], style=CWD_CURRENT)
    return text

def prompt(username, cwd):
    console.print(f"{username}@NyxOS", style=PROMPT, end="")
    console.print(format_cwd(cwd), end="")
    symbol = "#" if username == "root" else "$"
    return console.input(f"{symbol} ")

def run_shell(username):
    ctx = CommandContext(
        fs=fs,
        console=console,
        username=username
    )

    while True:
        line = prompt(username, fs.pwd())

        # --- parse redirection ---
        redirect_target = None
        if ">" in line:
            command_part, _, redirect_target = line.partition(">")
            redirect_target = redirect_target.strip()
            parts = command_part.split()
        else:
            parts = line.split()

        if not parts:
            continue

        cmd = parts[0].lower()
        args = parts[1:]

        handler = COMMANDS.get(cmd)
        if not handler:
            console.print(f"{cmd}: command not found", style=ERROR)
            continue

        try:
            result = handler(ctx, args)

            if isinstance(result, tuple):
                styled, plain = result
            else:
                styled = plain = result

        except ShellExit:
            break

        # --- output handling ---
        if redirect_target:
            if result is None:
                console.print("redirect: no output", style=ERROR)
            else:
                ctx.fs.write_file(redirect_target, plain)
        else:
            if result is not None:
                console.print(styled)