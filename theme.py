from colorama import Fore, Style, init

init(autoreset=True)

BANNER  = Fore.MAGENTA + Style.BRIGHT
PROMPT  = Fore.CYAN + Style.BRIGHT
TEXT    = Fore.WHITE
MUTED   = Fore.WHITE + Style.DIM
SUCCESS = Fore.GREEN + Style.BRIGHT
WARNING = Fore.YELLOW + Style.BRIGHT
ERROR   = Fore.RED + Style.BRIGHT
RESET   = Style.RESET_ALL