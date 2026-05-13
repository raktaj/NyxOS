# commands/__init__.py

import importlib
import pkgutil
from .registry import registry, CommandRegistry


def load_commands() -> CommandRegistry:
    package_name = __name__
    for _, module_name, _ in pkgutil.iter_modules(__path__):
        if module_name == "registry":
            continue
        importlib.import_module(f"{package_name}.{module_name}")
    return registry