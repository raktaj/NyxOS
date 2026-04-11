from rich.tree import Tree
from rich.text import Text

from themer import themer
from contracts import CommandOutput
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

    node_type = node.get("type")

    if node_type == "dir":
        children = node.get("children", {})

        for name, child in children.items():
            if child.get("type") == "dir":
                styled_name = f"[{themer.get('dir', 'rich')}]{name}/[/]"
                branch = tree.add(styled_name)
                build_tree(child, branch, max_depth, depth + 1)
            else:
                styled_name = f"[{themer.get('file', 'rich')}]{name}[/]"
                tree.add(styled_name)

# Commands

@command("cd")
def cmd_cd(ctx, args):
    if not args:
        return CommandOutput.err("cd: missing operand")
    try:
        new_path = ctx.fs.cd(args[0])
        return CommandOutput.text(new_path)
    except NotADirectoryError:
        return CommandOutput.err("cd: not a directory")
    except KeyError:
        return CommandOutput.err("cd: no such file or directory")


@command("shutdown", "exit", "quit")
def cmd_shutdown(ctx, args):
    raise ShellExit


@command("pwd")
def cmd_pwd(ctx, args):
    return CommandOutput.text(ctx.fs.pwd())

@command("ls")
def cmd_ls(ctx, args):
    try:
        path = args[0] if args else None
        node = ctx.fs.get_node(path)

        if node["type"] != "dir":
            return CommandOutput.err("ls: not a directory")

        children = node["children"]
        items = sorted(children.items(), key=lambda x: x[1]["type"] == "file")
        items = sorted(
            children.items(),
            key=lambda x: (x[1]["type"] == "file", x[0])
        )

        text = Text()

        for i, (name, child) in enumerate(items):
            if child["type"] == "dir":
                style = themer.get("dir", "rich")
                display = f"{name}/"
            else:
                style = themer.get("file", "rich")
                display = name

            # add newline only between items (not after last)
            if i < len(items) - 1:
                display += "\n"

            text.append(display, style=style)

        plain = "\n".join(children.keys())

        return CommandOutput(styled=text, plain=plain)

    except KeyError:
        return CommandOutput.err("ls: no such file or directory")

@command("rm")
def cmd_rm(ctx, args):
    if not args:
        return CommandOutput.err("rm: missing operand")

    recursive = False
    target = None

    if args[0] == "-r":
        if len(args) < 2:
            return CommandOutput.err("rm: missing operand")
        recursive = True
        target = args[1]
    else:
        target = args[0]

    try:
        ctx.fs.rm(target, recurse=recursive)
        return None
    except IsADirectoryError:
        return CommandOutput.err("rm: is a directory")
    except KeyError:
        return CommandOutput.err("rm: no such file or directory")


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
                return CommandOutput.err("tree: invalid depth")
        else:
            path = p

    try:
        node = ctx.fs.get_node(path)
    except KeyError:
        return CommandOutput.err("tree: no such file or directory")

    root_label = path if path else ctx.fs.pwd()
    tree = Tree(root_label, guide_style="dim")

    build_tree(node, tree, max_depth)
    return CommandOutput(styled=tree, plain=None)


@command("cat")
def cmd_cat(ctx, args):
    if not args:
        return CommandOutput.err("cat: missing operand")

    try:
        content = ctx.fs.cat(args[0])
        return CommandOutput.text(content)
    except IsADirectoryError:
        return CommandOutput.err("cat: is a directory")
    except KeyError:
        return CommandOutput.err("cat: no such file")


@command("clear")
def cmd_clear(ctx, args):
    # special signal handled by shell
    return CommandOutput(styled="__CLEAR__", plain=None)


@command("whoami")
def cmd_whoami(ctx, args):
    return CommandOutput.text(ctx.username)


@command("echo")
def cmd_echo(ctx, args):
    return CommandOutput.text(" ".join(args))


@command("help")
def cmd_help(ctx, args):
    from helpdata import HELP_ENTRIES

    text = Text()
    text.append("Available commands:\n")

    for cmd, desc in HELP_ENTRIES:
        text.append(f"  {cmd:<10} {desc}\n")

    return CommandOutput(styled=text, plain=None)


@command("mkdir")
def cmd_mkdir(ctx, args):
    if not args:
        return CommandOutput.err("mkdir: missing operand")
    try:
        ctx.fs.mkdir(args[0])
        return None
    except FileExistsError:
        return CommandOutput.err("mkdir: file exists")
    except KeyError:
        return CommandOutput.err("mkdir: invalid path")


@command("touch")
def cmd_touch(ctx, args):
    if not args:
        return CommandOutput.err("touch: missing operand")
    try:
        ctx.fs.touch(args[0])
        return None
    except KeyError:
        return CommandOutput.err("touch: invalid path")


@command("rmdir")
def cmd_rmdir(ctx, args):
    if not args:
        return CommandOutput.err("rmdir: missing operand")
    try:
        ctx.fs.rmdir(args[0])
        return None
    except NotADirectoryError:
        return CommandOutput.err("rmdir: not a directory")
    except KeyError:
        return CommandOutput.err("rmdir: no such directory")
    except OSError:
        return CommandOutput.err("rmdir: directory not empty")


from rich.columns import Columns
from rich.text import Text

@command("neofetch")
def cmd_neofetch(ctx, args):
    logo = f"""[{themer.get("banner", "rich")}]
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