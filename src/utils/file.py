import os
import json
import yaml
from typing import Dict, List

from chatgpt_cli import __version__
from utils.io import *


def get_data_dir(create=True) -> str:
    """Data directory: `${HOME}/.config/chatgpt-cli/data`"""
    data_dir = os.path.join(get_config_dir(), "data")
    if create and not os.path.exists(data_dir):
        os.mkdir(data_dir)
    return data_dir


def save_data(data: List[Dict[str, str]], filename: str) -> None:
    """Save list of dict to JSON file"""

    data_dir = get_data_dir()
    print("Data Directory: ", data_dir)

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


def import_data_directory():
    data_dir = get_data_dir()  # will create the data directory
    for i in range(3):
        try:
            old_data_dir = input(
                "Enter absolute path to the data directory containing *.json files (e.g., /absolute/path/to/data/): "
            ).strip()
            for file in os.listdir(old_data_dir):
                if file.endswith(".json"):
                    with open(os.path.join(old_data_dir, file), "r") as f:
                        data = json.load(f)
                    with open(os.path.join(data_dir, file), "w") as f:
                        json.dump(data, f)
            break
        except FileNotFoundError:
            printmd("**[File Not Found Error]**: Please check the path and try again")
        except Exception as e:
            printmd(f"**[Unknown Error]**: {e}")
    printmd(f"**[Success]**: Data files imported to `{data_dir}`")


def create_data_directory():
    data_dir = get_data_dir()  # will create the data directory
    printmd(f"**[Success]**: Data directory created at `{data_dir}`")


def get_config_dir() -> str:
    """Config directory: `${HOME}/.config/chatgpt-cli`"""
    config_dir = os.path.join(os.path.expanduser("~"), ".config", "chatgpt-cli")
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)
    return config_dir


def get_config_path() -> str:
    return os.path.join(get_config_dir(), "config.yaml")


def save_config_yaml(config: Dict):
    config_path = get_config_path()
    with open(config_path, "w") as f:
        yaml.dump(config, f, indent=2)
    printmd(f"**[Success]**: `config.yaml` file saved to `{config_path}`")


def import_config_yaml():
    config = None
    for i in range(3):
        try:
            config_path = input("Enter absolute path to `config.yaml` file: ").strip()
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
            break
        except FileNotFoundError:
            printmd("**[File Not Found Error]**: Please check the path and try again")
        except yaml.YAMLError:
            printmd("**[YAML Error]**: Please check the file and try again")
        except Exception as e:
            printmd(f"**[Unknown Error]**: {e}")

    if config is None:
        printmd("**[Error]**: Failed to import `config.yaml` file after 3 attempts")
        exit(1)

    save_config_yaml(config)


def create_config_yaml():
    config = {}
    config["openai"] = {}
    config["openai"]["api_key"] = input("Enter your OpenAI API key: ").strip()
    config["proxy"] = {}
    config["proxy"]["http_proxy"] = input(
        "Enter your HTTP proxy (leave blank if not needed): "
    ).strip()
    config["proxy"]["https_proxy"] = input(
        "Enter your HTTPS proxy (leave blank if not needed): "
    ).strip()
    config["openai"]["default_prompt"] = [
        {
            "role": "system",
            "content": "You are ChatGPT, a language model trained by OpenAI. Now you are responsible for answering any questions the user asks.",
        }
    ]
    save_config_yaml(config)


def load_config() -> Dict:
    # check if config file exists
    first_launch_msg = f"""
Welcome to ChatGPT CLI v{__version__}!

It looks like this is the first time you're using this tool.

To use the ChatGPT API you need to provide your OpenAI API key in the `{get_config_path()}` file.

You can create it manually or let this tool help you create it interactively.

You can also import an existing `config.yaml` file which is used in the script version of this tool.

If you don't have an OpenAI API key, you can get one at https://platform.openai.com/account/api-keys
"""
    # check setup
    config_path = get_config_path()
    if not os.path.exists(config_path):
        printpnl(first_launch_msg, "ChatGPT CLI Setup", "red", 120)
        choose = input(
            "Do you want to create a new `config.yaml` file or import an existing one? [y/i]: "
        ).strip()
        if choose.lower() == "i":
            import_config_yaml()
        else:
            create_config_yaml()
    # load configurations from config.yaml
    with open(config_path, "r") as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError:
            print("Error in configuration file:", config_path)
            exit(1)
    if not os.path.exists(get_data_dir(create=False)):
        choose = input(
            "Do you want to import previous data files [*.json]? [y/n]: "
        ).strip()
        if choose.lower() == "y":
            import_data_directory()
        else:
            create_data_directory()

    return config
