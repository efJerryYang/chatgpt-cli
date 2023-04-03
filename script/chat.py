import json
import os
import readline
from datetime import datetime
from typing import Dict, List

import openai
import yaml
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel


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
Welcome to ChatGPT CLI!

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
    print("Available data files:\n")
    for i, f in enumerate(files):
        print(f"{i + 1}. {f}")
    for a in range(3):
        selected_file = input(
            f"\nEnter file number to load (1-{len(files)}), or Enter to start a fresh one: "
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


class Conversation:
    def __init__(self, default_prompt: List[Dict[str, str]]) -> None:
        self.messages = list(default_prompt)
        self.default_prompt = list(default_prompt)
        self.filepath = load_data(self.messages)
        self.modified = False

    def __len__(self) -> int:
        return len(self.messages)

    def __add_message(self, message: Dict[str, str]) -> None:
        self.messages.append(message)
        self.modified = True

    def add_user_message(self, content: str) -> None:
        self.__add_message({"role": "user", "content": content})

    def add_assistant_message(self, content: str) -> None:
        self.__add_message({"role": "assistant", "content": content})

    def edit_system_message(self, content: str) -> None:
        if self.messages[0]["role"] == "system":
            self.messages[0]["content"] = content
            self.modified = True
        else:
            raise Exception("The first message is not a system message.")

    def save(self, enable_prompt: bool) -> None:
        if enable_prompt and self.modified:
            user_input = input("Save conversation? [y/n]: ").strip()
            if user_input.lower() != "y":
                printmd("**Conversation not saved.**")
                return

        if self.modified:
            if self.filepath:
                filename = os.path.basename(self.filepath)
            else:
                t = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                tmp = f"conversation_{t}.json"
                filename = input(f"Enter filename to save to [{tmp}]: ").strip()
                if not filename:
                    filename = tmp
                self.filepath = os.path.join(get_data_dir(), filename)
            printmd(f"**Conversation save to [{filename}].**")
            save_data(self.messages, filename)
            self.modified = False
        else:
            printmd("**Conversation not modified. Nothing to save.**")

    def load(self) -> None:
        if self.modified:
            user_input = input("Save conversation? [y/n]: ").strip()
            if user_input.lower() == "y":
                self.save(enable_prompt=False)
        self.messages = list(self.default_prompt)
        self.filepath = load_data(self.messages)
        self.modified = False
        printpnl("### Conversation loaded.", "ChatGPT CLI", "green", 120)

    def reset(self) -> None:
        if self.modified:
            user_input = input("Save conversation? [y/n]: ").strip()
            if user_input.lower() == "y":
                self.save(enable_prompt=False)
        self.filepath = ""
        self.messages = list(self.default_prompt)
        self.modified = False
        printpnl("### Conversation reset.", "ChatGPT CLI", "green", 120)

    def resend(self) -> None:
        self.resend_last_prompt()

    def resend_last_prompt(self) -> None:
        if len(self.messages) < 2:
            printmd("**No previous prompt to resend.**")
            return
        # Resend last prompt
        last_message = self.messages[-1]
        if last_message["role"] == "user":
            assistant_message = generate_response(self.messages)
            if not assistant_message:
                printmd("**Last response is empty. Resend failed.**")
                return
            self.add_assistant_message(assistant_message)
            printmd("**Last prompt resent.**")
            assistant_output(assistant_message)
        else:
            printmd("**Last message is assistant message. Nothing to resend.**")

    def regen(self) -> None:
        self.regenerate_last_response()

    def regenerate_last_response(self) -> None:
        """Regenerate last response"""
        if len(self.messages) < 2:
            printmd("**No previous response to regenerate.**")
            return
        # Regenerate last response
        last_message = self.messages[-1]
        if last_message["role"] == "user":
            printmd(
                "**Last message is user message. Nothing to regenerate. You may want to use `!resend` instead.**"
            )
            return
        content = generate_response(self.messages[:-1])
        if not content:
            printmd("**Last response is empty. Content not regenerated.**")
            return
        self.__fill_content(-1, content)
        assistant_output(self.messages[-1]["content"])
        printmd("**Last response regenerated.**")

    def __fill_content(self, index: int, content: str) -> None:
        """Fill content"""
        self.messages[index]["content"] = content
        self.modified = True

    def __edit_message(self, index: int, prompt=True) -> None:
        """Edit message"""
        if prompt:
            msg = self.messages[index]
            printpnl(f"### Editing Message {index}", "Editing Messages", "yellow")
            show_message(msg)
        new_content = user_input("\nEnter new content, leave blank to skip: ")
        if new_content:
            self.__fill_content(index, new_content)
            printmd("**Message edited.**")
        else:
            printmd("**Message not edited.**")

    def show_history(self, index=False, panel=True):
        """Show conversation history"""
        if panel:
            printpnl("### Messages History", "ChatGPT CLI", "green")
        if index:
            for i in range(len(self.messages)):
                printpnl(f"### Message {i}", "Messages History", "green")
                show_message(self.messages[i])
        else:
            for message in self.messages:
                show_message(message)

    def edit_messages(self) -> None:
        """Edit messages"""
        if len(self.messages) == 0:
            printmd("**No message to edit.**")
            return
        # Show messages history with index to select, or iterate through them one by one?
        choose = input(
            "Show messages history with [i]ndex to select, or iterate [t]hrough them one by one? [i/t]: "
        ).strip()
        if choose.lower() == "i":
            # Show messages history with index to select
            printpnl("### Messages History", "Editing Messages", "yellow")
            self.show_history(index=True, panel=False)
            index = (
                input(
                    "Enter index of messages to edit, separate with comma (e.g. 0,1,2), leave blank to cancel: "
                )
                .strip()
                .strip(",")
            )
            if not index:
                printmd("**Editing cancelled.**")
                return
            try:
                index = [int(i.strip()) for i in index.split(",")]
                for i in index:
                    if i >= len(self.messages):
                        raise ValueError
            except ValueError:
                printmd("**Invalid index. Editing cancelled.**")
                return
            for i in index:
                self.__edit_message(i, prompt=True)
        else:  # choose.lower() == "o":
            for i in range(len(self.messages)):
                self.__edit_message(i, prompt=True)

    def drop_messages(self) -> None:
        """Drop messages"""
        if len(self.messages) == 0:
            printmd("**No message to drop.**")
            return
        index = []
        for i, msg in enumerate(self.messages):
            printpnl(f"### Message {i}", "Dropping Messages", "yellow")
            show_message(msg)
            user_input = input("Select this message to drop? [y/n]: ").strip()
            if user_input.lower() == "y":
                index.append(i)
                printmd("**Message selected.**")
            else:
                printmd("**Message not selected.**")
        if index:
            for i in reversed(index):
                printpnl(f"### Message {i}", "Dropping Messages", "red")
                show_message(self.messages[i])
                user_input = input("Drop this message? [y/n]: ").strip()
                if user_input.lower() == "y":
                    self.messages.pop(i)
                    self.modified = True
                    printmd("**Message dropped.**")
                else:
                    printmd("**Message not dropped.**")
            printmd("**Selected messages dropped.**")
        else:
            printmd("**No message selected. Dropping cancelled.**")


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


console = Console()


def printmd(msg: str, newline=True) -> None:
    console.print(Markdown(msg))
    if newline:
        print()


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
    msg = "\n".join(lines)
    printmd("**[Input Submitted]**")
    return msg


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
- `!new` or `!reset`: start a new conversation
- `!regen`: regenerate the last response
- `!resend`: resend your last prompt to generate response
- `!edit`: select messages to edit
- `!drop`: select messages to drop
- `!exit` or `!quit`: exit the program

You can enter these commands at any time during a conversation when you are prompted with `User:`.

For more detailed documentation, please visit <link_to_wiki> or <link_to_docs>

Enjoy your chat!
"""
    printpnl(welcome_msg, title="Welcome")


def generate_response(messages: List[Dict[str, str]]) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-3.5-turbo-0301
            messages=messages,
        )
        assistant_message = response["choices"][0]["message"]["content"].strip()
        return assistant_message
    except openai.error.APIConnectionError as api_conn_err:
        print(api_conn_err)
        printpnl(
            "**[API Connection Error]**\n. Please check your internet connection and try again."
        )
        user_message = input("Do you want to retry now? (y/n): ")
        if user_message.strip().lower() == "y":
            return generate_response(messages)
        else:
            return ""
    except openai.error.InvalidRequestError as invalid_err:
        print(invalid_err)
        printpnl(
            "**[Invalid Request Error]**\nPlease revise your messages according to the error message above."
        )
        return ""
    except openai.error.APIError as api_err:
        print(api_err)
        printpnl(
            "**[API Error]**\nThis might be caused by API outage. Please try again later."
        )
        user_message = input("Do you want to retry now? (y/n): ")
        if user_message.strip().lower() == "y":
            return generate_response(messages)
        else:
            return ""
    except openai.error.RateLimitError as rate_err:
        print(rate_err)
        printpnl(
            "**[Rate Limit Error]**\nThis is caused by API outage. Please try again later."
        )
        user_message = input("Do you want to retry now? (y/n): ")
        if user_message.strip().lower() == "y":
            return generate_response(messages)
        else:
            return ""
    except Exception as e:
        print(e)
        printpnl(
            "**[Unknown Error]**\nThis is an unknown error, please contact maintainer with error message to help handle it properly."
        )
        return ""


if __name__ == "__main__":
    config = setup_runtime_env()
    default_prompt = config["openai"]["default_prompt"]
    show_welcome_panel()

    conv = Conversation(default_prompt)
    conv.show_history()

    while True:
        user_message = user_input().strip()
        if is_command(user_message):
            execute_command(user_message, conv)
            continue
        else:
            conv.add_user_message(user_message)
        assistant_message = generate_response(conv.messages)
        if assistant_message:
            assistant_output(assistant_message)
            conv.add_assistant_message(assistant_message)
            continue
        else:
            conv.save(True)
