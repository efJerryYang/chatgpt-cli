import openai
import os

from chatgpt_cli.conversation import generate_response
from utils.cmd import *
from utils.file import *
from utils.io import *


def get_script_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


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
        elif type(default_prompt) is not list:
            raise (
                Exception("Error: the `default_prompt` is not a list in `config.yaml`")
            )
    except Exception:
        print("Error in configuration file:", get_config_path())
        exit(1)
    return config


def read_message(conv, tmpl):
    user_message = user_input()
    if user_message == "":
        return

    if is_command(user_message):
        execute_command(user_message, conv, tmpl)
        return
    conv.add_user_message(user_message)

    assistant_message = generate_response(conv.messages)
    if assistant_message:
        assistant_output(assistant_message)
        conv.add_assistant_message(assistant_message)
        return
    conv.save(True)


def loop(conv, tmpl):
    try:
        read_message(conv, tmpl)
    except KeyboardInterrupt as e:
        input_error_handler(conv.modified, e)
    except EOFError as e:
        input_error_handler(conv.modified, e)


def main():
    config = setup_runtime_env()
    default_prompt = config["openai"]["default_prompt"]
    show_welcome_panel()

    conv = Conversation(default_prompt)
    conv.show_history()
    tmpl = Template()
    while True:
        loop(conv, tmpl)


if __name__ == "__main__":
    main()
