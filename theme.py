# theme.py
from rich.style import Style

PROMPT = Style(color="cyan", bold=True)
MUTED  = Style(color="bright_black")
TEXT   = Style(color="white")
ERROR  = Style(color="red", bold=True) 
SUCCESS = Style(color="green")
BANNER = Style(color="magenta", bold=True)

CWD_PARENT  = Style(color="magenta")
CWD_CURRENT = Style(color="magenta", bold=True)
CWD_SEP = Style(color="magenta")
