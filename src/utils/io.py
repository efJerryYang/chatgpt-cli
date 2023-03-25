import readline
from typing import Dict

from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from chatgpt_cli import __version__

console = Console()


def print(*args, **kwargs) -> None:
    console.print(*args, **kwargs)


def printpnl(
    msg: str, title="ChatGPT CLI", border_style="white", width=120, markdown=True
) -> None:
    print()
    if markdown:
        print(Panel(Markdown(msg), title=title, border_style=border_style, width=width))
    else:
        print(Panel(msg, title=title, border_style=border_style, width=width))
    print()


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


def user_input(prompt="\nUser: ") -> str:
    """
    Get user input with support for multiple lines without submitting the message.
    """
    # Use readline to handle user input
    lines = []
    while True:
        line = input(prompt)
        if line.strip() == "":
            break
        lines.append(line)
        # Update the prompt using readline
        prompt = "\r" + " " * len(prompt) + "\r" + " .... " + readline.get_line_buffer()
    # Print a message indicating that the input has been submitted
    msg = "\n".join(lines).strip()
    if msg:
        printmd("**[Input Submitted]**")
    else:
        printmd("**[Empty Input Skipped]**")
    return msg


def show_welcome_panel():
    welcome_msg = f"""
Welcome to ChatGPT CLI v{__version__}!

Greetings! Thank you for choosing this CLI tool. This tool is generally developed for personal use purpose. We use OpenAI's official API to interact with the ChatGPT, which would be more stable than the web interface.

This tool is still under development, and we are working on improving the user experience. If you have any suggestions, please feel free to open an issue on our GitHub: https://github.com/efJerryYang/chatgpt-cli/issues

Here are some useful commands you may want to use:

- `!help`: show this message
- `!show`: show current conversation messages
- `!save`: save current conversation to a `JSON` file
- `!load`: load a conversation from a `JSON` file
- `!new` or `!reset`: start a new conversation
- `!regen`: regenerate the last response
- `!resend`: resend your last prompt to generate response
- `!edit`: select messages to edit
- `!drop`: select messages to drop
- `!exit` or `!quit`: exit the program

Features (under development):
- `!tmpl` or `!tmpl load`: select a template to use
- `!tmpl show`: show all templates with complete information
- `!tmpl create`: create a new template
- `!tmpl edit`: edit an existing template (not implemented yet)
- `!tmpl drop`: drop an existing template (not implemented yet)

You can enter these commands at any time during a conversation when you are prompted with `User:`.

For more detailed documentation, please visit <link_to_wiki> or <link_to_docs>

Enjoy your chat!
"""
    printpnl(welcome_msg, title="Welcome")


def show_setup_error_panel(config_path: str):
    first_launch_msg = f"""
Welcome to ChatGPT CLI v{__version__}!

It looks like this is the first time you're using this tool.

To use the ChatGPT API you need to provide your OpenAI API key in the `{config_path}` file.

You can create it manually or let this tool help you create it interactively.

You can also import an existing `config.yaml` file which is used in the script version of this tool.

If you don't have an OpenAI API key, you can get one at https://platform.openai.com/account/api-keys
"""
    printpnl(first_launch_msg, "ChatGPT CLI Setup", "red", 120)
