# commands/pwd.py

from contracts import CommandOutput
from .registry import command

@command("pwd", help="print working directory", usage="pwd")
def cmd_pwd(ctx, args):
    return CommandOutput.text(ctx.fs.pwd())