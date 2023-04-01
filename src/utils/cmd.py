from chatgpt_cli.conversation import Conversation, Template
from utils.io import *
import re


def is_command(user_msg: str) -> bool:
    """Check if user input is a command"""
    quit_words = ["quit", "exit"]
    return user_msg.startswith("!") or user_msg in quit_words


def execute_command(
    user_msg: str,
    conv: Conversation,
    tmpl: Template,
) -> str:
    user_msg = user_msg.strip()
    if user_msg in ["!help", "help", "!h"]:
        show_welcome_panel()
    elif user_msg in ["!show", "show"]:
        conv.show_history()
    elif user_msg in ["!save", "save"]:
        conv.save(False)
    elif user_msg in ["!load", "load"]:
        conv.load()
        conv.show_history(panel=False)
    elif user_msg in ["!new", "new", "reset", "!reset"]:
        conv.reset()
        conv.show_history(panel=False)
    elif user_msg in ["!editor", "editor", "!e"]:
        message = input_from_editor()
        user_msg += " " + message
    elif user_msg in ["!resend", "resend"]:
        conv.resend()
    elif user_msg in ["!regen", "regen"]:
        conv.regen()
    elif user_msg in ["!edit", "edit"]:
        conv.edit_messages()
    elif user_msg in ["!drop", "drop"]:
        conv.drop_messages()
    elif user_msg in ["!exit", "!quit", "quit", "exit", "!q"]:
        conv.save(True)
        print("Bye!")
        exit(0)
    elif user_msg.startswith("!tmpl"):
        tmpl.execute_command(user_msg, conv)
    elif user_msg.startswith("!"):
        print("Invalid command, please try again")
    return user_msg


def post_command_process(user_message):
    # handle the return string of execute_command
    pattern = re.compile(r"^!\w*\s*")
    if user_message.startswith("!e ") or user_message.startswith("!editor "):
        user_message = pattern.sub("", user_message)
        user_output(user_message)
        if not user_message:
            printmd("**[Empty Input Skipped]**")
    else:
        user_message = pattern.sub("", user_message)
    return user_message
