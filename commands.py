# commands.py
from rich.tree import Tree
from rich.text import Text

from theme import TEXT, ERROR, MUTED
from shell_exceptions import ShellExit




COMMANDS = {}

def command(*names):
    def decorator(func):
        for name in names:
            COMMANDS[name] = func
        return func
    return decorator

def build_tree(node, tree, max_depth, depth=0):
    if max_depth is not None and depth >= max_depth:
        return

    if not isinstance(node, dict):
        return

    for name, child in node.items():
        if isinstance(child, dict):
            branch = tree.add(f"[bold]{name}[/]")
            build_tree(child, branch, max_depth, depth + 1)
        else:
            tree.add(name)

# Command Contract
# @command("cmdname")
# def cmd_cmdname(ctx, args) -> str | Text | Tree | None

@command("cd")
def cmd_cd(ctx, args):
    if not args:
        ctx.console.print("cd: missing operand", style=ERROR)
        return None
    try:
        ctx.console.print(ctx.fs.cd(args[0]))
    except NotADirectoryError:
        ctx.console.print("cd: not a directory", style=ERROR)
    except KeyError:
        ctx.console.print("cd: no such file or directory", style=ERROR)

@command("shutdown", "exit")
def cmd_shutdown(ctx, args):
    raise ShellExit

@command("pwd")
def cmd_pwd(ctx, args): 
    return ctx.fs.pwd()

@command("ls")
def cmd_ls(ctx, args):
    try:
        path = args[0] if args else None
        return "\n".join(ctx.fs.ls(path))
    except NotADirectoryError:
        ctx.console.print("ls: not a directory", style=ERROR)
    except KeyError:
        ctx.console.print("ls: no such file or directory", style=ERROR)
    return True

@command("rm")
def cmd_rm(ctx, args):
    if not args:
        ctx.console.print("rm: missing operand", style=ERROR)
        return None

    recursive = False
    target = None

    if args[0] == "-r":
        if len(args) < 2:
            ctx.console.print("rm: missing operand", style=ERROR)
            return None
        recursive = True
        target = args[1]
    else:
        target = args[0]

    try:
        ctx.fs.rm(target, recurse=recursive)
    except IsADirectoryError:
        ctx.console.print("rm: is a directory", style=ERROR)
    except KeyError:
        ctx.console.print("rm: no such file or directory", style=ERROR)
    return None

@command("tree")
def cmd_tree(ctx, args):
    max_depth = None
    path = None

    parts_iter = iter(args)
    for p in parts_iter:
        if p == "-L":
            try:
                max_depth = int(next(parts_iter))
            except (StopIteration, ValueError):
                ctx.console.print("tree: invalid depth", style=ERROR)
                return None
        else:
            path = p

    try:
        node = ctx.fs.get_node(path)
    except KeyError:
        ctx.console.print("tree: no such file or directory", style=ERROR)
        return None

    root_label = path if path else ctx.fs.pwd()
    tree = Tree(root_label, guide_style="dim")

    build_tree(node, tree, max_depth)
    return tree

@command("cat")
def cmd_cat(ctx, args):
    if not args:
        ctx.console.print("cat: missing operand", style=ERROR)
        return None

    try:
        return ctx.fs.cat(args[0])
    except IsADirectoryError:
        ctx.console.print("cat: is a directory", style=ERROR)
    except KeyError:
        ctx.console.print("cat: no such file", style=ERROR)
    return None

@command("clear")
def cmd_clear(ctx, args):
    ctx.console.clear()
    return None

@command("whoami")
def cmd_whoami(ctx, args):
    return ctx.username

@command("echo")
def cmd_echo(ctx, args):
    return " ".join(args)


@command("help")
def cmd_help(ctx, args):
    from helpdata import HELP_ENTRIES

    text = Text()
    text.append("Available commands:\n", style=TEXT)

    for cmd, desc in HELP_ENTRIES:
        text.append(f"  {cmd:<10} {desc}\n", style=MUTED)

    return text

@command("mkdir")
def cmd_mkdir(ctx, args):
    if not args:
        ctx.console.print("mkdir: missing operand", style=ERROR)
        return None
    try:
        ctx.fs.mkdir(args[0])
    except FileExistsError:
        ctx.console.print("mkdir: file exists", style=ERROR)
    except KeyError:
        ctx.console.print("mkdir: invalid path", style=ERROR)
    return None

@command("touch")
def cmd_touch(ctx, args):
    if not args:
        ctx.console.print("touch: missing operand", style=ERROR)
        return None
    try:
        ctx.fs.touch(args[0])
    except KeyError:
        ctx.console.print("touch: invalid path", style=ERROR)

    return None

@command("rmdir")
def cmd_rmdir(ctx, args):
    if not args:
        ctx.console.print("rmdir: missing operand", style=ERROR)
        return None
    try:
        ctx.fs.rmdir(args[0])
    except NotADirectoryError:
        ctx.console.print("rmdir: not a directory", style=ERROR)
    except KeyError:
        ctx.console.print("rmdir: no such directory", style=ERROR)
    except OSError:
        ctx.console.print("rmdir: directory not empty", style=ERROR)
    return None

@command("neofetch")
def cmd_neofetch(ctx, args):
    logo_styled = """[bold magenta]
███╗   ██╗██╗   ██╗██╗  ██╗ ██████╗ ███████╗
████╗  ██║╚██╗ ██╔╝╚██╗██╔╝██╔═══██╗██╔════╝
██╔██╗ ██║ ╚████╔╝  ╚███╔╝ ██║   ██║███████╗
██║╚██╗██║  ╚██╔╝   ██╔██╗ ██║   ██║╚════██║
██║ ╚████║   ██║   ██╔╝ ██╗╚██████╔╝███████║
╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝[/]
"""

    info_lines = [
        ("OS",        "NyxOS"),
        ("User",      ctx.username),
        ("Shell",     "nsh"),
        ("Kernel",    "nyx-kernel 0.2"),
        ("Uptime",    "unknown"),
        ("Packages",  "builtin"),
        ("Theme",     "Nyx Magenta"),
        ("Terminal",  "Rich Console"),
    ]

    # ----- styled output (interactive) -----
    styled_lines = [logo_styled]
    for key, val in info_lines:
        styled_lines.append(f"[bold]{key}[/]: {val}")

    styled_output = "\n".join(styled_lines)

    # ----- plain output (redirection) -----
    plain_lines = ["NyxOS"]
    for key, val in info_lines:
        plain_lines.append(f"{key}: {val}")

    plain_output = "\n".join(plain_lines)

    # IMPORTANT: return, do not print
    return styled_output, plain_output