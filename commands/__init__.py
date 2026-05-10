# commands/__init__.py

import importlib
import pkgutil
from .registry import COMMANDS

def load_commands():
    package_name = __name__

    for _, module_name, _ in pkgutil.iter_modules(__path__):
        if module_name == "registry":
            continue  # skip registry module

        importlib.import_module(f"{package_name}.{module_name}")
        
    return COMMANDS