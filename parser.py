# parser.py

from dataclasses import dataclass, field

@dataclass
class ParsedArgs:
    flags: dict[str, bool] = field(default_factory=dict)
    options: dict[str, str] = field(default_factory=dict)
    positionals: list[str] = field(default_factory=list)

@dataclass
class ArgumentSpec:
    flags: set[str] | None = None           # e.g. {"r"}
    options: set[str] | None = None         # e.g. {"L"}

def parse_args(tokens: list[str], spec: ArgumentSpec | None) -> ParsedArgs:
    parsed = ParsedArgs()

    if spec is None:
        parsed.positionals = tokens
        return parsed

    i = 0
    while i < len(tokens):
        tok = tokens[i]

        if tok.startswith("-") and len(tok) > 1:
            key = tok.lstrip("-")

            # flag
            if spec.flags and key in spec.flags:
                parsed.flags[key] = True
                i += 1
                continue

            # option (takes value)
            if spec.options and key in spec.options:
                if i + 1 >= len(tokens):
                    raise ValueError(f"-{key} requires a value")
                parsed.options[key] = tokens[i + 1]
                i += 2
                continue

            raise ValueError(f"unknown flag: {tok}")

        # positional
        parsed.positionals.append(tok)
        i += 1

    return parsed