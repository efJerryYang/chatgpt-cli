import os
import json
import readline
from datetime import datetime

import openai
import yaml
from rich.console import Console
from rich.markdown import Markdown


# load configurations from config.yaml
dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(dir, "config.yaml")
with open(config_path, "r") as f:
    try:
        config = yaml.safe_load(f)
    except yaml.YAMLError:
        print("Error in configuration file:", config_path)
        exit(1)

openai.api_key = config["openai"]["api_key"]
default_prompt = config["openai"]["default_prompt"]
# set proxy
os.environ["http_proxy"] = config["proxy"]["http_proxy"]
os.environ["https_proxy"] = config["proxy"]["https_proxy"]


def save_data(data, filename):
    # save list of dict to JSON file
    currdir = os.path.dirname(os.path.abspath(__file__))
    print("current: ", currdir)
    datadir = os.path.join(currdir, "data")

    if not os.path.exists(datadir):
        os.mkdir(datadir)
    # if filename end with json
    if filename.endswith(".json"):
        filepath = os.path.join(datadir, filename)
    else:
        filepath = os.path.join(datadir, filename + ".json")
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filepath}")


def load_data(default_prompt):
    currdir = os.path.dirname(os.path.abspath(__file__))
    print("current: ", currdir)
    datadir = os.path.join(currdir, "data")
    if not os.path.exists(datadir):
        os.mkdir(datadir)
    # list all JSON files in the 'data' directory
    files = [f for f in os.listdir("data") if f.endswith(".json")]
    if not files:
        print("No data files found in 'data' directory")
        return "", default_prompt
    # prompt user to select a file to load
    print("Available data files:")
    for i, f in enumerate(files):
        print(f"{i+1}. {f}")
    selected_file = input(
        f"Enter file number to load (1-{len(files)}), or Enter to start a fresh one: "
    )
    if not selected_file:
        return "", default_prompt
    # validate user input and load the selected file
    try:
        index = int(selected_file) - 1
        if not 0 <= index < len(files):
            raise ValueError()
        filepath = os.path.join("data", files[index])
        with open(filepath, "r") as f:
            data = json.load(f)
        print(f"Data loaded from {filepath}")
        return filepath, data
    except (ValueError, IndexError):
        print("Invalid input, please try again")
        return load_data(default_prompt)


console = Console()


def printmd(msg: str) -> None:
    console.print(Markdown(msg))


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
        prompt = "\r" + " " * len(prompt) + "\r" + ".... " + readline.get_line_buffer()
    # Print a message indicating that the input has been submitted
    print("[Input Submitted]\n")
    return "\n".join(lines)


def user_output(msg: str) -> None:
    printmd("**User:** {}".format(msg))


def assistant_output(msg: str) -> None:
    printmd("**ChatGPT:** {}".format(msg))


def system_output(msg: str) -> None:
    printmd("**System:** {}".format(msg))


filepath, messages = load_data(default_prompt)

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

# select to response to the conversation or start a new one
response = input(
    "Continue the conversation? You can also ask a follow up question. (y[es]/a[sk]/n[o]/q[uit]): "
)
if response.lower() in ["n", "no"]:
    messages = default_prompt
    print("Starting a new conversation...")
elif response.lower() in ["a", "ask"]:
    print("Ask a follow up question...")
    user_message = user_input()
    messages.append({"role": "user", "content": user_message})
elif response.lower() in ["q", "quit"]:
    print("Exiting...")
    exit()
else:
    print("Continuing the conversation...")

while True:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or gpt-3.5-turbo-0301
        messages=messages,
    )
    assistant_message = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": assistant_message})
    # printmd("**ChatGPT:** {}".format(assistant_message))
    assistant_output(assistant_message)
    user_message = user_input()
    if user_message in ["quit", "exit", "q"]:
        t = f"{datetime.now():%Y-%m-%d_%H:%M:%S}"
        # Do you want to save the conversation?
        save = input(f"Do you want to save the conversation? (y[es]/n[o]): ")
        if save.lower() in ["n", "no"]:
            print("Exiting...")
            break
        if not filepath:
            filename = input(f"Enter a filename to save to (default to '{t}.json'): ")
            filename = t if not filename.strip() else filename.strip()
            save_data(messages, filename)
            break
        # filepath is not empty, ask if user wants to save to the same file
        save = input(f"Save to the same file? (y[es]/n[o]): ")
        if save.lower() in ["n", "no"]:
            filename = input(
                f"Enter a filename to save to (default to '{t}.json'), or Enter 'exit' to exit: "
            )
            filename = t if not filename.strip() else filename.strip()
            save_data(messages, filename)
            break
        filename = os.path.basename(filepath)
        save_data(messages, filename)
        break
    messages.append({"role": "user", "content": user_message})
