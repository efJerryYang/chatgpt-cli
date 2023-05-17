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


def read_message(conv, tmpl, use_streaming):
    user_message = user_input()

    if is_command(user_message):
        printmd("**[Command Executed]**")
        user_message = execute_command(user_message, conv, tmpl)
        user_message = post_command_process(user_message)

    if user_message == "":
        return

    conv.add_user_message(user_message)
    printmd("**[Input Submitted]**")

    if use_streaming == True:
        assistant_message = assistant_stream(generate_response(conv.messages, use_streaming))
    else:
        assistant_message = "".join(list(generate_response(conv.messages, use_streaming)))

    if assistant_message:
        if use_streaming == False: assistant_output(assistant_message)
        conv.add_assistant_message(assistant_message)
    else:
        conv.save(True)


def loop(conv, tmpl, use_streaming):
    try:
        read_message(conv, tmpl, use_streaming)
    except KeyboardInterrupt as e:
        input_error_handler(conv.modified, e)
    except EOFError as e:
        input_error_handler(conv.modified, e)


def main():
    config = setup_runtime_env()
    use_streaming = config.get('chat', {}).get('use_streaming', False)

    default_prompt = config["openai"]["default_prompt"]
    show_welcome_panel()

    conv = Conversation(default_prompt, use_streaming)
    conv.show_history()

    tmpl = Template()
    while True:
        loop(conv, tmpl, use_streaming)


if __name__ == "__main__":
    main()
