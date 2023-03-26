from chatgpt_cli.conversation import Conversation, Template
from utils.io import *


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
    if user_msg in ["!help", "help"]:
        show_welcome_panel()
        user_msg = ""
    elif user_msg in ["!show", "show"]:
        conv.show_history()
        user_msg = ""
    elif user_msg in ["!save", "save"]:
        conv.save(False)
        user_msg = ""
    elif user_msg in ["!load", "load"]:
        conv.load()
        conv.show_history(panel=False)
        user_msg = ""
    elif user_msg in ["!new", "new", "reset", "!reset"]:
        conv.reset()
        conv.show_history(panel=False)
        user_msg = ""
    elif user_msg in ["!resend", "resend"]:
        conv.resend()
        user_msg = ""
    elif user_msg in ["!regen", "regen"]:
        conv.regen()
        user_msg = ""
    elif user_msg in ["!edit", "edit"]:
        conv.edit_messages()
        user_msg = ""
    elif user_msg in ["!drop", "drop"]:
        conv.drop_messages()
        user_msg = ""
    elif user_msg in ["!editor", "editor"]:
        message = input_from_editor()
        user_msg = message
    elif user_msg in ["!exit", "!quit", "quit", "exit"]:
        conv.save(True)
        user_msg = ""
        print("Bye!")
        exit(0)
    elif user_msg.startswith("!tmpl"):
        tmpl.execute_command(user_msg, conv)
        user_msg = ""
    elif user_msg.startswith("!"):
        print("Invalid command, please try again")
        user_msg = ""
    return user_msg
