import os
import sys
import tempfile
import readline
import subprocess
from typing import Dict
from chatgpt_cli import __version__

from output.print import *
from output.panel import *


def input_error_handler(is_modified: bool, e: Exception) -> None:
    initial_error = e
    for i in range(3):
        try:
            if isinstance(e, EOFError):
                printmd("**[EOF Error]**", newline=False)
                printmd("**Exiting...**", newline=False)
                exit(0)
            elif isinstance(e, KeyboardInterrupt):
                printmd("**[Keyboard Interrupted Error]**", newline=False)
                printpnl(
                    "### You have interrupted the program with `Ctrl+C`. This is usually caused by pressing `Ctrl+C`.",
                    "Exit Confirmation",
                    "red",
                )
                confirm_prompt = f"Are you sure you want to exit{' without saving' if is_modified else ''}? [Y/n]: "
                if input(confirm_prompt).lower() == "y":
                    printmd("**Exiting...**", newline=False)
                    exit(0)
                else:
                    printmd("**[Resuming]**")
                    return
            else:
                printmd(
                    "**[Unknown Error]** This a an unhandled error. Please report this issue on GitHub: https://github.com/efJerryYang/chatgpt-cli/issues"
                )
                raise e
        except Exception as e:
            continue


def input_from_editor() -> str:
    editor = os.environ.get("EDITOR", "vim")
    initial_message = b""

    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        tf.write(initial_message)
        tf.flush()

        subprocess.call([editor, tf.name])

        tf.seek(0)
        msg = tf.read().decode().strip()
        return msg


def user_input(prompt="\nUser: ") -> str:
    """
    Get user input with support for multiple lines without submitting the message.
    """
    # Use readline to handle user input
    lines = []
    while True:
        line = input(prompt).strip()
        if line == "":
            break
        lines.append(line)
        if lines[0].startswith("!"):
            break
        # Update the prompt using readline
        prompt = "\r" + " " * len(prompt) + "\r" + " .... "
        readline.get_line_buffer()
    # Print a message indicating that the input has been submitted
    msg = "\n\n".join(lines).strip()
    if not msg:
        printmd("**[Empty Input Skipped]**")
    return msg
