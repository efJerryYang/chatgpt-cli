from typing import Dict
from chatgpt_cli import __version__

from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()


def printpnl(
    msg: str, title="ChatGPT CLI", border_style="white", width=120, markdown=True
) -> None:
    print()
    if markdown:
        print(Panel(Markdown(msg), title=title, border_style=border_style, width=width))
    else:
        print(Panel(msg, title=title, border_style=border_style, width=width))
    print()


def show_welcome_panel():
    welcome_msg = f"""
Welcome to ChatGPT CLI v{__version__}!

Greetings! Thank you for choosing this CLI tool. This tool is generally developed for personal use purpose. We use OpenAI's official API to interact with the ChatGPT, which would be more stable than the web interface.

This tool is still under development, and we are working on improving the user experience. If you have any suggestions, please feel free to open an issue on our GitHub: https://github.com/efJerryYang/chatgpt-cli/issues

Here are some useful commands you may want to use:

- `!help` or `!h`: show this message
- `!show`: show current conversation messages
- `!save`: save current conversation to a `JSON` file
- `!load`: load a conversation from a `JSON` file
- `!new` or `!reset`: start a new conversation
- `!editor` or `!e`: use your default editor (e.g. vim) to submit a message
- `!regen`: regenerate the last response
- `!resend`: resend your last prompt to generate response
- `!edit`: select messages to edit
- `!drop`: select messages to drop
- `!exit` or `!quit` or `!q`: exit the program

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

def show_dirty_config_panel(config_path: str, missing_keys: list):
    """
    Prompt the user to update their config file if it is outdated.
    """
    dirty_config_msg = f"""
It looks like your config file is not up-to-date at `{config_path}`.

The following keys are missing in your config file:

{missing_keys}

Notice that even if you don't need some of the optional key values, it is always recommended to add

at least keys with empty values to your `config.yaml` file.
"""
    printpnl(dirty_config_msg, "ChatGPT CLI Update Config", "yellow", 120)
