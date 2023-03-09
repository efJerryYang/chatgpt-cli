from datetime import datetime
import json
import os
import readline
from typing import Dict, List

import openai
import yaml
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich import print


from chatgpt_cli import __version__
from chatgpt_cli.conversation import Conversation
from utils.io import *



def is_command(user_input: str) -> bool:
    """Check if user input is a command"""
    quit_words = ["quit", "exit"]
    return user_input.startswith("!") or user_input in quit_words


def execute_command(
    user_input: str,
    conv: Conversation,
) -> str:
    user_input = user_input.strip()
    if user_input in ["!help", "help"]:
        show_welcome_panel()
    elif user_input in ["!show", "show"]:
        conv.show_history()
    elif user_input in ["!save", "save"]:
        conv.save(False)
    elif user_input in ["!load", "load"]:
        conv.load()

        conv.show_history(panel=False)
    elif user_input in ["!new", "new", "reset", "!reset"]:
        conv.reset()
        conv.show_history(panel=False)
    elif user_input in ["!resend", "resend"]:
        conv.resend()
    elif user_input in ["!regen", "regen"]:
        conv.regen()
    elif user_input in ["!edit", "edit"]:
        conv.edit_messages()
    elif user_input in ["!drop", "drop"]:
        conv.drop_messages()
    elif user_input in ["!exit", "!quit", "quit", "exit"]:
        conv.save(True)
        print("Bye!")
        exit(0)
    elif user_input.startswith("!"):
        print("Invalid command, please try again")
    return user_input
