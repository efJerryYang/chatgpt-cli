from datetime import datetime
from typing import List

import openai
import os

from utils.file import *


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


class Conversation:
    def __init__(self, default_prompt: List[Dict[str, str]]) -> None:
        self.messages = list(default_prompt)
        self.default_prompt = list(default_prompt)
        self.filepath = ""
        self.modified = False
        self.template_object = Template()

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
                t = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
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
            confirm = input("Select this message to drop? [y/n]: ").strip()
            if confirm.lower() == "y":
                index.append(i)
                printmd("**Message selected.**")
            else:
                printmd("**Message not selected.**")
        if index:
            for i in reversed(index):
                printpnl(f"### Message {i}", "Dropping Messages", "red")
                show_message(self.messages[i])
                confirm = input("Drop this message? [y/n]: ").strip()
                if confirm.lower() == "y":
                    self.messages.pop(i)
                    self.modified = True
                    printmd("**Message dropped.**")
                else:
                    printmd("**Message not dropped.**")
            printmd("**Selected messages dropped.**")
        else:
            printmd("**No message selected. Dropping cancelled.**")

    def switch_template(self, id):
        """Switch template"""
        self.template_object.id = id
        roles = [msg['role'] for msg in self.template_object.templates[id]["prompts"]]
        if 'system' in roles:
            self.default_prompt = list(self.template_object.templates[id]["prompts"])
        else:
            self.default_prompt.extend(list(self.template_object.templates[id]["prompts"]))
        printmd(f"**Template switched to {self.template_object.get_name()}.**")


"""
Features (under development):
- `!tmpl`: select a template to use
- `!tmpl show`: show all templates with complete information
- `!tmpl create`: create a new template
- `!tmpl edit`: edit an existing template
- `!tmpl drop`: drop an existing template
"""


class Template:
    def __init__(self) -> None:
        self.templates = self.__load_templates()
        self.id = None

    def get_name(self) -> str:
        return self.templates[self.id]["name"]

    def __load_templates(self) -> List[Dict]:
        return load_templates()

    def __parse_command(self, cmd: str) -> List[str]:
        cmd = cmd.strip()
        if cmd.startswith("!tmpl"):
            cmd = cmd[5:].strip()
        else:
            raise ValueError(f"Invalid command {cmd} for template")
        return cmd.split()

    def execute_command(self, cmd: str, conv: Conversation):
        cmd = self.__parse_command(cmd)
        if not cmd or cmd[0] == "load":
            self.load(conv=conv)
        elif cmd[0] == "show":
            self.show()
        elif cmd[0] == "create":
            self.create()
        elif cmd[0] == "edit":
            self.edit()
        elif cmd[0] == "drop":
            self.drop()
        else:
            printmd("**[Error]: Invalid command.**")

    def show(self, only_name: bool = False):
        print("Config Directory:", get_config_dir())
        print(f"Templates (in {get_patch_path()}):\n")
        if only_name:
            for i, t in enumerate(self.templates):
                print(f"{i + 1}. {t['name']} ({t['alias']})")
            return
        for i, t in enumerate(self.templates):
            print(f"{i + 1}. {t['name']} ({t['alias']})")
            print(f"    Description: {t['description']}")
            print(f"    Messages:")
            for j, p in enumerate(t["prompts"]):
                print(f"      {j}. {p['role']}: {p['content']}")
            print(f"    References:")
            for j, r in enumerate(t["references"]):
                print(f"      {j}. {r['role']}: {r['content']}")
            print()

    def create(self):
        update_patch(create_template)

    def edit(self):
        update_patch(edit_template)

    def drop(self):
        update_patch(drop_template)

    def load(self, conv: Conversation):
        self.show(only_name=True)
        for i in range(3):
            try:
                selected_id = input(
                    "\nPlease select a template (leave blank to skip): "
                ).strip()
                if not selected_id:
                    printmd("**No template selected.**")
                    return
                self.id = int(selected_id) - 1
                if self.id < 0 or self.id >= len(self.templates):
                    raise ValueError
                conv.switch_template(self.id)
                conv.reset()
                conv.show_history()
                return
            except ValueError:
                print("Invalid template id, please try again")
            except KeyboardInterrupt:
                print()
                return
            except EOFError:
                printmd("**[EOF Error]: Aborting")
                exit(1)
        print("Too many invalid inputs, not switching template")
        return
