# commands/tree.py

from contracts import CommandOutput
from .registry import command
from parser import ArgumentSpec

from rich.tree import Tree

def build_tree(themer, node, tree, max_depth, depth=0):
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
                build_tree(themer, child, branch, max_depth, depth + 1)
            else:
                styled_name = f"[{themer.get('file', 'rich')}]{name}[/]"
                tree.add(styled_name)

@command(
    "tree",
    help="display directory tree",
    usage="tree [-L depth] [path]",
    argspec=ArgumentSpec(options={"L"})
)
def cmd_tree(ctx, args):
    max_depth = None

    if "L" in args.options:
        try:
            max_depth = int(args.options["L"])
        except ValueError:
            return CommandOutput.err("tree: invalid depth")

    path = args.positionals[0] if args.positionals else None

    try:
        node = ctx.fs.get_node(path)
    except NyxError as e:
        return CommandOutput.err("tree: no such file or directory")

    root_label = path if path else ctx.fs.pwd()
    tree = Tree(root_label, guide_style="dim")

    build_tree(ctx.themer, node, tree, max_depth)
    return CommandOutput(styled=tree, plain=None)