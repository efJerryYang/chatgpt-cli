from typing import Dict
from chatgpt_cli import __version__

from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()


def print(*args, **kwargs) -> None:
    console.print(*args, **kwargs)


def printmd(msg: str, newline=True) -> None:
    console.print(Markdown(msg))
    if newline:
        print()


def show_message(msg: Dict[str, str]) -> None:
    role = msg["role"]
    content = msg["content"]
    if role == "user":
        user_output(content)
    elif role == "assistant":
        assistant_output(content)
    elif role == "system":
        system_output(content)
    else:
        raise ValueError(f"Invalid role: {role}")


def user_output(msg: str) -> None:
    printmd("**User:** {}".format(msg))


def assistant_output(msg: str) -> None:
    printmd("**ChatGPT:** {}".format(msg))


def system_output(msg: str) -> None:
    printmd("**System:** {}".format(msg))
