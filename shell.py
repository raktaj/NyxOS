from rich.console import Console
from prompt_toolkit import prompt as prompt_input
from prompt_toolkit.formatted_text import FormattedText

import shlex

from themer import format_cwd, themer
from commands import COMMANDS
from contracts import CommandContext, CommandOutput
from fs import FileSystem
from shell_exceptions import ShellExit

console = Console()
fs = FileSystem()

def build_prompt(username, cwd):
    symbol = "#" if username == "root" else "$"

    formatted = []

    # Username
    formatted.append((themer.prompt("prompt_user"), f"{username}@NyxOS"))

    # CWD (delegated)
    cwd_parts = format_cwd(cwd, themer, engine="prompt")
    formatted.extend(cwd_parts)

    # Symbol
    formatted.append(("", f"{symbol} "))

    return FormattedText(formatted)

def parse_command(line):
    try:
        tokens = shlex.split(line)
    except ValueError as e:
        console.print(f"parse error: {e}", style=themer.rich("error"))
        return None, None, None

    if not tokens:
        return None, None, None

    redirect_target = None
    clean_tokens = []

    it = iter(tokens)
    for token in it:
        if token == ">":
            try:
                redirect_target = next(it)
            except StopIteration:
                console.print("redirect: missing target", style=themer.rich("error"))
                return None, None, None
            break
        else:
            clean_tokens.append(token)

    cmd = clean_tokens[0]
    args = clean_tokens[1:]
    return cmd, args, redirect_target


def run_shell(username):
    ctx = CommandContext(fs=fs, username=username)

    while True:
        prompt_fmt = build_prompt(username, fs.pwd())
        line = prompt_input(prompt_fmt)

        cmd, args, redirect_target = parse_command(line)
        if not cmd:
            continue

        handler = COMMANDS.get(cmd)
        if not handler:
            console.print(f"{cmd}: command not found", style=themer.rich("error"))
            continue

        try:
            result = handler(ctx, args)
        except ShellExit:
            break

        if result is None:
            continue

        if not isinstance(result, CommandOutput):
            result = CommandOutput.text(str(result))

        # special clear handling
        if result.styled == "__CLEAR__":
            console.clear()
            continue

        # error handling
        if result.error:
            console.print(result.styled, style=themer.rich("error"))
            continue

        # redirection
        if redirect_target:
            if result.plain is None:
                console.print("redirect: no output", style=themer.rich("error"))
            else:
                fs.write_file(redirect_target, result.plain)
        else:
            if result.styled is not None:
                console.print(result.styled)