# themer.py

import json
from pathlib import Path
from rich.style import Style
from rich.text import Text
from typing import overload, Literal

class Themer:
    def __init__(self, theme_path="themes.json"):
        self.theme_path = Path(theme_path)
        self.theme = self._load_theme()
        self._validate()

    # Internal

    def _load_theme(self):
        if not self.theme_path.exists():
            raise FileNotFoundError(f"Theme file not found: {self.theme_path}")

        with open(self.theme_path, "r") as f:
            return json.load(f)

    def _validate(self):
        required_keys = {"rich", "prompt"}

        for name, styles in self.theme.items():
            if not isinstance(styles, dict):
                raise ValueError(f"{name} must be an object")

            missing = required_keys - styles.keys()
            if missing:
                raise ValueError(f"{name} missing keys: {missing}")

    # Adapters
    def rich(self, name):
        return Style.parse(self.theme[name]["rich"])

    def prompt(self, name):
        return self.theme[name]["prompt"]

    def get(self, name, engine):
        return self.theme[name][engine]

@overload
def format_cwd(
    cwd: str,
    themer: Themer,
    engine: Literal["prompt"]
) -> list[tuple[str, str]]: ...

@overload
def format_cwd(
    cwd: str,
    themer: Themer,
    engine: Literal["rich"]
) -> Text: ...

def format_cwd(
    cwd: str,
    themer: Themer,
    engine: Literal["prompt", "rich"] = "rich"
) -> Text | list[tuple[str, str]]:

    parts = [p for p in cwd.split("/") if p]

    if engine == "rich":
        text = Text()

        if not parts:
            text.append("/", style=themer.rich("cwd_current"))
            return text

        for part in parts[:-1]:
            text.append("/", style=themer.rich("cwd_sep"))
            text.append(part, style=themer.rich("cwd_parent"))

        text.append("/", style=themer.rich("cwd_sep"))
        text.append(parts[-1], style=themer.rich("cwd_current"))

        return text

    elif engine == "prompt":
        formatted = []

        if not parts:
            formatted.append((themer.prompt("cwd_current"), "/"))
            return formatted

        for part in parts[:-1]:
            formatted.append((themer.prompt("cwd_parent"), f"/{part}"))

        formatted.append((themer.prompt("cwd_current"), f"/{parts[-1]}"))
        return formatted
    else:
        raise ValueError(f"Unknown engine: {engine}")

themer = Themer()