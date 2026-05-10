# shell.py

from rich.console import Console
from prompt_toolkit import prompt as prompt_input
from prompt_toolkit.formatted_text import FormattedText

import shlex
from dataclasses import dataclass
from typing import Optional

from utils import render_command_help
from themer import format_cwd
from contracts import CommandContext, CommandOutput
from errors import ShellExit, NyxError, SwitchUser
from parser import parse_args

console = Console()


@dataclass
class Session:
    username: str


def build_prompt(username, cwd, themer):
    symbol = "#" if username == "root" else "$"

    formatted = []

    # Username
    formatted.append((themer.prompt("prompt_user"), f"{username}@NyxOS"))

    # CWD
    cwd_parts = format_cwd(cwd, themer, engine="prompt")
    formatted.extend(cwd_parts)

    # Symbol
    formatted.append(("", f"{symbol} "))

    return FormattedText(formatted)


def parse_command(line: str) -> tuple[Optional[str], list[str], Optional[str]]:
    try:
        tokens = shlex.split(line)
    except ValueError as e:
        raise ValueError(f"parse error: {e}")

    if not tokens:
        return None, [], None

    redirect_target = None
    clean_tokens = []
    it = iter(tokens)
    for token in it:
        if token == ">":
            try:
                redirect_target = next(it)
            except StopIteration:
                raise ValueError("redirect: missing target")
            break
        else:
            clean_tokens.append(token)

    cmd = clean_tokens[0]
    args = clean_tokens[1:]
    return cmd, args, redirect_target


def run_shell(username, fs, themer, commands, user_store):
    session = Session(username=username)
    ctx = CommandContext(fs=fs, username=session.username, themer=themer, user_store=user_store)

    while True:
        prompt_fmt = build_prompt(session.username, fs.pwd(), themer)
        line = prompt_input(prompt_fmt)

        try:
            cmd, args, redirect_target = parse_command(line)
        except ValueError as e:
            console.print(str(e), style=themer.rich("error"))
            continue

        if not cmd:
            continue

        # rebuild ctx if user has changed
        ctx = CommandContext(fs=fs, username=session.username, themer=themer, user_store=user_store)

        cmd_obj = commands.get(cmd)
        if not cmd_obj:
            console.print(f"{cmd}: command not found", style=themer.rich("error"))
            continue

        if any(a in ("--help", "-h") for a in args):
            help_text = render_command_help(cmd_obj)
            console.print(help_text)
            continue

        try:
            parsed_args = parse_args(args, cmd_obj.argspec)
        except ValueError as e:
            console.print(str(e), style=themer.rich("error"))
            continue

        try:
            result = cmd_obj.handler(ctx, parsed_args)
        except SwitchUser as e:
            session.username = e.username
            fs.username = e.username
            fs.cwd = f"/home/{e.username}"
            continue
        except ShellExit:
            break
        except NyxError as e:
            console.print(str(e), style=themer.rich("error"))
            continue
        except Exception as e:
            console.print(f"internal error: {e}", style=themer.rich("error"))
            continue

        if result is None:
            continue

        if not isinstance(result, CommandOutput):
            result = CommandOutput.text(str(result))

        if result.styled == "__CLEAR__":
            console.clear()
            continue

        if redirect_target:
            if result.plain is None:
                console.print("redirect: no output", style=themer.rich("error"))
            else:
                try:
                    fs.write_file(redirect_target, result.plain)
                except NyxError as e:
                    console.print(str(e), style=themer.rich("error"))
        else:
            console.print(result.styled)