from datetime import datetime
import json
import os
import readline
import sys
from typing import Dict, Tuple, List

import openai
import yaml
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich import print


def get_script_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def get_data_dir() -> str:
    return os.path.join(get_script_dir(), "data")


def get_config_dir() -> str:
    return get_script_dir()


def get_config_path() -> str:
    return os.path.join(get_config_dir(), "config.yaml")


def printpnl(
    msg: str, title="ChatGPT CLI", border_style="white", width=120, markdown=True
) -> None:
    print()
    if markdown:
        print(Panel(Markdown(msg), title=title, border_style=border_style, width=width))
    else:
        print(Panel(msg, title=title, border_style=border_style, width=width))
    print()


def load_config() -> Dict:
    # check if config file exists
    first_launch_msg = """
# Welcome to ChatGPT CLI!

It looks like this is the first time you're using this tool.

To use the ChatGPT API you need to provide your OpenAI API key in the `config.yaml` file.

To get started, please follow these steps:

1. Copy the `config.yaml.example` file to `config.yaml` in the same directory.
2. Open `config.yaml` using a text editor an replace `<YOUR_API_KEY>` with your actual OpenAI API key.
3. Optionally, you can also set a default prompt to use for generating your GPT output.

If you don't have an OpenAI API key, you can get one at https://platform.openai.com/account/api-keys/.

Once you've configured your `config.yaml` file, you can start this tool again.

Thank you for using ChatGPT CLI!
"""
    # check setup
    config_path = get_config_path()
    if not os.path.exists(config_path):
        printpnl(first_launch_msg, "ChatGPT CLI Setup", "red", 120)
        exit(1)
    # load configurations from config.yaml
    with open(config_path, "r") as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError:
            print("Error in configuration file:", config_path)
            exit(1)
    return config


def setup_runtime_env() -> Dict:
    config = load_config()
    try:
        # set up openai API key and system prompt
        openai.api_key = config["openai"]["api_key"]
        # set proxy if defined
        if "proxy" in config:
            os.environ["http_proxy"] = config["proxy"].get("http_proxy", "")
            os.environ["https_proxy"] = config["proxy"].get("https_proxy", "")
            default_prompt = config.get("openai", {}).get("default_prompt", None)
        if default_prompt is None:
            raise (Exception("Error: the `default_prompt` is empty in `config.yaml`"))
    except Exception:
        print("Error in configuration file:", get_config_path())
        exit(1)
    return config


def is_command(user_input: str) -> bool:
    """Check if user input is a command"""
    quit_words = ["quit", "exit"]
    return user_input.startswith("!") or user_input in quit_words


def save_current_conversation(
    messages: List[Dict[str, str]],
    filepath: str,
    default_prompt: List[Dict[str, str]],
    enable_prompt: bool = True,
) -> None:
    """Save current conversation to a file"""
    # Ask user to make sure they want to save
    if enable_prompt:
        user_message = input("Do you want to save this conversation? [y/n]: ")
        if user_message.lower() == "n":
            printmd("**Conversation not saved.**")
            return
    # Check if this conversation is the same as the default_prompt
    if is_same_message(messages, default_prompt):
        printmd(
            "**This conversation is the same as the default prompt. Nothing to save.**"
        )
        return
    # Save conversation
    if filepath:
        save_data(messages, os.path.basename(filepath))
    else:
        t = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        tmp = f"conversation_{t}.json"
        filename = input(f"Enter filename to save to [{tmp}]: ").strip()
        if not filename:
            filename = tmp
        save_data(messages, filename)
    printmd("**Conversation saved.**")


def load_existing_conversation(
    messages: List[Dict[str, str]], default_prompt: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    messages.clear()
    messages.extend(list(default_prompt))
    return load_data(messages)


def start_new_converstation(
    messages: List[Dict[str, str]], default_prompt: List[Dict[str, str]]
) -> None:
    messages.clear()
    messages.extend(list(default_prompt))


def regenerate_last_response(messages: List[Dict[str, str]]):
    """Regenerate last response"""
    last_msg = messages[-1]
    if last_msg["role"] == "user":
        printmd("**You can't regenerate your own response. You may want to drop it first.**")
        return
    # Regenerate last response
    messages[-1]["content"] = generate_response(messages)
    assistant_output(messages[-1]["content"])
    printmd("**Last response regenerated.**")


def edit_messages(messages: List[Dict[str, str]]) -> None:
    for i in range(len(messages)):
        msg = messages[i]
        printpnl(
            f"{i}. {msg['role']}: {msg['content']}\n", "Editing Messages", "yellow"
        )
        print("Enter new message (or Enter to skip).")
        new_msg = user_input()
        if new_msg:
            messages[i]["content"] = new_msg
            printmd("**Message updated.**\n")
        else:
            printmd("**Message not updated.**\n")
    printpnl("## Done.", "Editing Messages", "white", 120)


def select_from_messages(messages: List[Dict[str, str]]) -> List[int]:
    index_list = []
    for i, msg in enumerate(messages):
        printpnl(
            f"{i}. {msg['role']}: {msg['content']}\n", "Selecting Messages", "yellow"
        )
        index = input("Select this message to drop? [y/n]: ").strip()
        if index.lower() == "y":
            index_list.append(i)
            printmd("**Message selected.**\n")
        else:
            printmd("**Message not selected.**\n")
    return index_list


def drop_selected_messages(messages: list[Dict[str, str]], index_list: List[int]):
    for i in sorted(index_list, reverse=True):
        msg = messages[i]
        printpnl(f"{i}. {msg['role']}: {msg['content']}\n", "Dropping Messages", "yellow")
        index = input("Drop this message? [y/n]: ").strip()
        if index.lower() == "y":
            messages.pop(i)
            printmd("**Message dropped.**\n")
        else:
            printmd("**Message not dropped.**\n")
    printpnl("## Done.", "Dropping Messages", "white", 120)


def execute_command(
    user_input: str,
    messages: List[Dict[str, str]],
    filepath: str,
    default_prompt: List[Dict[str, str]],
) -> str:
    user_input = user_input.strip()
    if user_input == "!help":
        show_welcome_panel()
    elif user_input == "!show":
        display_history(messages)
    elif user_input == "!save":
        # examine whether the conetent is the same as default_prompt
        # ask user to check if save current file
        save_current_conversation(messages, filepath, default_prompt, False)
    elif user_input == "!load":
        save_current_conversation(messages, filepath, default_prompt)
        filepath = load_existing_conversation(messages, default_prompt)
        display_history(messages)
    elif user_input == "!new":
        save_current_conversation(messages, filepath, default_prompt)
        start_new_converstation(messages, default_prompt)
        display_history(messages)
    elif user_input == "!regen":
        regenerate_last_response()
    elif user_input == "!edit":
        edit_messages(messages)
    elif user_input == "!drop":
        index_list = select_from_messages(messages)
        drop_selected_messages(messages, index_list)
    elif user_input in ["!exit", "!quit", "quit", "exit"]:
        save_current_conversation(messages, filepath, default_prompt)
        print("Bye!")
        exit(0)
    elif user_input.startswith("!"):
        print("Invalid command, please try again")
    return user_input


def save_data(data: List[Dict[str, str]], filename: str) -> None:
    """Save list of dict to JSON file"""

    data_dir = get_data_dir()
    print("Data Directory: ", data_dir)
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    if filename.endswith(".json"):
        filepath = os.path.join(data_dir, filename)
    else:
        filepath = os.path.join(data_dir, filename + ".json")
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filepath}")


def load_data(messages: List[Dict[str, str]]) -> str:
    """Load JSON file from 'data' directory to 'messages', and return the filepath"""

    data_dir = get_data_dir()
    print("Data Directory: ", data_dir)
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    files = [f for f in os.listdir(data_dir) if f.endswith(".json")]
    if not files:
        print("No data files found in 'data' directory")
        return ""

    # prompt user to select a file to load
    print("Available data files:")
    for i, f in enumerate(files):
        print(f"{i+1}. {f}")
    for a in range(3):
        selected_file = input(
            f"Enter file number to load (1-{len(files)}), or Enter to start a fresh one: "
        )
        if not selected_file.strip():
            return ""
        try:
            index = int(selected_file) - 1
            if not 0 <= index < len(files):
                raise ValueError()
            filepath = os.path.join(data_dir, files[index])
            with open(filepath, "r") as f:
                data = json.load(f)
                messages.clear()
                messages.extend(data)
            print(f"Data loaded from {filepath}")
            return filepath
        except (ValueError, IndexError):
            print("Invalid input, please try again")
    print("Too many invalid inputs, aborting")
    exit(1)


console = Console()


def printmd(msg: str, newline=True) -> None:
    console.print(Markdown(msg))
    if newline:
        print()


def user_input() -> str:
    """
    Get user input with support for multiple lines without submitting the message.
    """
    # Use readline to handle user input
    prompt = "\nUser: "
    lines = []
    while True:
        line = input(prompt)
        if line.strip() == "":
            break
        lines.append(line)
        # Update the prompt using readline
        prompt = "\r" + " " * len(prompt) + "\r" + " .... " + readline.get_line_buffer()
    # Print a message indicating that the input has been submitted
    msg = "\n".join(lines)
    # handle msg in execute_command
    # user_output(msg + "\n**[Input Submitted]**")
    printmd("**[Input Submitted]**")
    return msg


def user_output(msg: str) -> None:
    printmd("**User:** {}".format(msg))


def assistant_output(msg: str) -> None:
    printmd("**ChatGPT:** {}".format(msg))


def system_output(msg: str) -> None:
    printmd("**System Prompt to ChatGPT:** {}".format(msg))


def show_welcome_panel():
    welcome_msg = """
Welcome to ChatGPT CLI!

Greetings! Thank you for choosing this CLI tool. This tool is generally developed for personal use purpose. We use OpenAI's official API to interact with the ChatGPT, which would be more stable than the web interface.

This tool is still under development, and we are working on improving the user experience. If you have any suggestions, please feel free to open an issue on our GitHub: https://github.com/efJerryYang/chatgpt-cli/issues

Here are some useful commands you may want to use:

- `!help`: show this message
- `!show`: show current conversation messages
- `!save`: save current conversation to a `JSON` file
- `!load`: load a conversation from a `JSON` file
- `!new`: start a new conversation
- `!regen`: regenerate the last response
- `!edit`: select a message to edit
- `!drop`: select a message to drop
- `!exit` or `!quit`: exit the program

You can enter these commands at any time during a conversation when you are prompted with `User:`.

For more detailed documentation, please visit <link_to_wiki> or <link_to_docs>

Enjoy your chat!
"""
    printpnl(welcome_msg, title="Welcome")


def display_history(messages: List[Dict[str, str]]) -> None:
    print()
    for msg in messages:
        if msg["role"] == "user":
            # printmd("**User:** {}".format(msg["content"]))
            user_output(msg["content"])
        elif msg["role"] == "assistant":
            # console.print(Markdown("**ChatGPT:** {}".format(msg["content"])))
            assistant_output(msg["content"])
        else:  # system
            # console.print(Markdown("**System:** {}".format(msg["content"])))
            system_output(msg["content"])
        # newline
        console.print()


def is_same_message(
    msg_list1: List[Dict[str, str]], msg_list2: List[Dict[str, str]]
) -> bool:
    if len(msg_list1) != len(msg_list2):
        return False
    for i in range(len(msg_list1)):
        if (
            msg_list1[i]["role"] != msg_list2[i]["role"]
            or msg_list1[i]["content"] != msg_list2[i]["content"]
        ):
            return False
    return True


def generate_response(messages: List[Dict[str, str]]) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-3.5-turbo-0301
            messages=messages,
        )
        assistant_message = response["choices"][0]["message"]["content"].strip()
        return assistant_message
    except openai.error.APIConnectionError as api_err:
        print(api_err)
        user_message = input(
            "Oops, something went wrong. Do you want to retry? (y/n): "
        )
        if user_message.strip().lower() == "y":
            return generate_response(messages)
        else:
            return ""
    except openai.error.InvalidRequestError as invalid_err:
        print(invalid_err)
        printpnl("**[Invalid Request]**\nPlease revise your messages according to the error message above.")
        return ""

if __name__ == "__main__":
    config = setup_runtime_env()
    default_prompt = config["openai"]["default_prompt"]
    show_welcome_panel()
    messages = default_prompt.copy()

    filepath = load_data(messages)
    display_history(messages)

    while True:
        user_message = user_input().strip()
        if is_command(user_message):
            execute_command(user_message, messages, filepath, default_prompt)
            continue
        else:
            messages.append({"role": "user", "content": user_message})

        assistant_message = generate_response(messages)
        if assistant_message:
            assistant_output(assistant_message)
            messages.append({"role": "assistant", "content": assistant_message})
            continue
        else:
            save_current_conversation(messages, filepath, default_prompt)
