from typing import Callable, Dict, List
import os
import json
import yaml

from chatgpt_cli import __version__

from output.color_print import *
from output.panel import *
from input.input import *


def get_data_dir(create=True) -> str:
    """Data directory: `${HOME}/.config/chatgpt-cli/data`"""
    data_dir = os.path.join(get_config_dir(), "data")
    if create and not os.path.exists(data_dir):
        os.makedirs(data_dir)
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
        try:
            selected_file = input(
                f"\nEnter file number to load (1-{len(files)}), or Enter to start a fresh one: "
            )
            if not selected_file.strip():
                return ""
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
        except (KeyboardInterrupt, EOFError):
            print("Aborting")
            exit(1)
    print_warning("Warning: Too many invalid inputs, starting a fresh one")
    return ""


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
            print_warning("File Not Found Error: Please check the path and try again")
        except Exception as e:
            print_error(f"Unknown Error: {e}")
    print_success(f"Success: Data files imported to `{data_dir}`")


def create_data_directory():
    data_dir = get_data_dir()  # will create the data directory
    print_success(f"Success: Data directory created at `{data_dir}`")


def get_config_dir() -> str:
    """Config directory: `${HOME}/.config/chatgpt-cli`"""
    config_dir = os.path.join(os.path.expanduser("~"), ".config", "chatgpt-cli")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    return config_dir


def get_config_path() -> str:
    return os.path.join(get_config_dir(), "config.yaml")


def save_config_yaml(config: Dict):
    config_path = get_config_path()
    with open(config_path, "w") as f:
        yaml.dump(config, f, indent=2)
    print_success(f"Success: `config.yaml` file saved to `{config_path}`")


def import_config_yaml():
    config = None
    for i in range(3):
        try:
            config_path = input("Enter absolute path to `config.yaml` file: ").strip()
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
            break
        except FileNotFoundError:
            print_error("File Not Found Error: Please check the path and try again")
        except yaml.YAMLError:
            print_error("YAML Error: Please check the file and try again")
        except Exception as e:
            print_error(f"Unknown Error: {e}")

    if config is None:
        print_error("Error: Failed to import `config.yaml` file after 3 attempts")
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
    # TODO: add prompt to setup code theme, give a list of available themes and display a preview
    config["theme"] = {}
    config["theme"]["code_theme"] = "monokai"
    save_config_yaml(config)


def setup_new_config():
    config_path = get_config_path()
    show_setup_error_panel(config_path)

    choose = input(
        "Do you want to create a new `config.yaml` file or import an existing one? [y/i]: "
    ).strip()
    if choose.lower() == "i":
        import_config_yaml()
    else:
        create_config_yaml()


def update_dirty_config(config: Dict, missing_keys: List[str]) -> None:
    config_path = get_config_path()
    show_dirty_config_panel(config_path, missing_keys)

    # Prompt the user to setup the missing keys
    for key in missing_keys:
        if key == "openai":
            config["openai"] = {}
            config["openai"]["api_key"] = input("Enter your OpenAI API key: ").strip()
            config["openai"]["default_prompt"] = [
                {
                    "role": "system",
                    "content": "You are ChatGPT, a language model trained by OpenAI. Now you are responsible for answering any questions the user asks.",
                }
            ]
        elif key == "proxy":
            config["proxy"] = {}
            config["proxy"]["http_proxy"] = input(
                "Enter your HTTP proxy (leave blank if not needed): "
            ).strip()
            config["proxy"]["https_proxy"] = input(
                "Enter your HTTPS proxy (leave blank if not needed): "
            ).strip()
        elif key == "theme":
            config["theme"] = {}
            config["theme"]["code_theme"] = "monokai"
        else:
            config[key] = {}
            print_warning(f"Warning: Unknown key `{key}` found in your `config.yaml`")
    # Store the updated config
    save_config_yaml(config)


def load_config() -> Dict[str, Dict]:
    # check setup
    config_path = get_config_path()
    if not os.path.exists(config_path):
        setup_new_config()
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
    # check if the config is up to date
    if check_config_data(config):
        return config
    else:
        return load_config()


def check_config_data(config: Dict[str, Dict]) -> bool:
    """
    Ensure that the `config.yaml` is up to date. If it is not, then prompt to
    update it.
    """
    # TODO: add more checks for specific keys, for example, `openai.api_key`
    missing_keys = []
    if config.get("openai", "") == "":
        print("The section `openai` is not configured", config)
        missing_keys.append("openai")
    if config.get("proxy", "") == "":
        print("The section `proxy` is not configured", config)
        missing_keys.append("proxy")
    if config.get("theme", "") == "":
        print("The section `theme` is not configured", config)
        missing_keys.append("theme")
    if missing_keys:
        update_dirty_config(config, missing_keys)
        return False
    return True


def load_patch() -> Dict:
    """Load the patch file"""
    patch_path = get_patch_path()
    with open(patch_path, "r") as f:
        try:
            patch = yaml.safe_load(f)
        except yaml.YAMLError:
            print("Error in patch file:", patch_path)
            exit(1)
    return patch


def get_patch_path():
    patch_path = os.path.join(get_config_dir(), "patch.yaml")
    if not os.path.exists(patch_path):
        with open(patch_path, "w") as f:
            yaml.dump({}, f, indent=2)
    return patch_path


def save_patch(patch: Dict):
    """Save the patch file"""
    patch_path = os.path.join(get_config_dir(), "patch.yaml")
    with open(patch_path, "w") as f:
        yaml.dump(patch, f, indent=2)
    print_success(f"Success: `patch.yaml` file saved to `{patch_path}`")


def update_patch(operation: Callable):
    patch = load_patch()
    operation(patch)
    save_patch(patch=patch)


def create_template(patch: Dict):
    """Create a new template in the `patch.yaml` file"""
    template_name = input("Enter template name: ").strip()
    if template_name == "":
        print_error("Error: Template name cannot be empty")
        return
    template_alias = input("Enter template alias (leave blank to skip): ").strip()
    if template_alias == "":
        template_alias = None
    template_list = patch.get("templates", [])
    for template in template_list:
        if template["name"] == template_name:
            print_error(
                f"Error: Template `{template_name}` already exists, pick another name"
            )
            return
        if template_alias is not None and template["alias"] == template_alias:
            print_warning(
                f"Warning: Template alias `{template_alias}` already exists, leaving it blank..."
            )
            template_alias = None

    template = {}
    template["name"] = template_name
    template["alias"] = template_alias if template_alias is not None else ""
    template["description"] = input(
        "Enter a simple template description (leave blank to skip): "
    ).strip()
    template["prompts"] = []
    while True:
        try:
            printpnl("### Add a new prompt (leave blank to skip)")
            role = input("Enter prompt role system/user/assistant [s/u/a]: ").strip()
            if role == "":
                break
            r = role.lower()
            if r in ["s", "system"]:
                role = "system"
            elif r in ["u", "user"]:
                role = "user"
            elif r in ["a", "assistant"]:
                role = "assistant"
            else:
                print_error(f"Error: Invalid role `{role}`, please try again")
                continue
            message = {}
            message["role"] = role
            message["content"] = user_input(
                f"Enter prompt content for [{role}]: "
            ).strip()
            template["prompts"].append(message)
        except KeyboardInterrupt as e:
            input_error_handler(True, e)
            continue
        except EOFError as e:
            input_error_handler(True, e)
            continue
    if len(template["prompts"]) == 0:
        print_warning("Warning: No prompts added, nothing to save")
        return
    # add reference
    check = input("Do you want to add references to the template? [y/n]: ").strip()
    if check.lower() == "y":
        template["references"] = []
        while True:
            try:
                printpnl("### Add a new reference (leave blank to skip)")
                reference = {}
                reference["url"] = input("Enter reference url: ").strip()
                if reference["url"] == "":
                    break
                reference["title"] = input("Enter reference title: ").strip()
                if reference["title"] == "":
                    print_warning("Warning: Reference title is empty, skipping...")
                template["references"].append(reference)
            except KeyboardInterrupt as e:
                input_error_handler(True, e)
                continue
            except EOFError as e:
                input_error_handler(True, e)
                continue
    else:
        template["references"] = [{"url": "", "title": ""}]
    # save to file
    template_list.append(template)
    patch["templates"] = template_list
    print_success(f"Success: Template `{template_name}` created")


def load_templates() -> List[Dict]:
    """Load the templates from the `patch.yaml` file"""
    patch = load_patch()
    return patch.get("templates", [])


def edit_template(patch: Dict):
    print_error("Error: Not implemented yet")


def drop_template(patch: Dict):
    print_error("Error: Not implemented yet")
