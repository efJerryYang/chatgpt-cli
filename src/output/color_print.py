from chatgpt_cli import __version__

import colorama
from colorama import Fore, Style

colorama.init()


def print_error(message):
    print(f"{Fore.RED}{message}{Style.RESET_ALL}")


def print_warning(message):
    print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")


def print_notice(message):
    print(f"{Fore.BLUE}Notice:{Style.RESET_ALL} {message}")


def print_info(message):
    print(f"{Fore.CYAN}{Style.RESET_ALL} {message}")


def print_success(message):
    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
