import os
from typing import Dict, List

import openai
import yaml
from rich import print

from utils.conversation import *
from utils.display import *
from utils.command import *


def get_script_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def get_config_dir() -> str:
    return get_script_dir()


def get_config_path() -> str:
    return os.path.join(get_config_dir(), "config.yaml")


def load_config() -> Dict:
    # check setup
    config_path = get_config_path()
    if not os.path.exists(config_path):
        show_setup_error_panel()
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
