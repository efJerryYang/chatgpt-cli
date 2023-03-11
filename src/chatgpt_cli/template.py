from typing import List, Dict

import os

from utils.file import *
from chatgpt_cli.conversation import Conversation

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
        if cmd[0] == "show":
            self.show()
        elif cmd[0] == "create":
            self.create()
        elif cmd[0] == "edit":
            self.edit()
        elif cmd[0] == "drop":
            self.drop()
        else:
            self.load(conv=conv)

    def show(self, only_name: bool = False):
        if only_name:
            print("Templates:")
            for i, t in enumerate(self.templates):
                print(f"{i + 1}. {t['name']} ({t['alias']})")
            return
        print("Templates:")
        for i, t in enumerate(self.templates):
            print(f"{i + 1}. {t['name']} ({t['alias']})")
            print(f"    {t['id']}")
            print(f"    {t['description']}")
            print(f"    {t['prompts']}")
            for j, p in enumerate(t["prompts"]):
                print(f"    {j}. {p['role']}: {p['content']}")
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
                template_id = int(input("Please select a template: "))
                self.id = template_id
                if template_id < 1 or template_id > len(self.templates):
                    raise ValueError
                conv.switch_template(self.templates[template_id - 1].copy())
            except ValueError:
                print("Invalid template id, please try again")
            except KeyboardInterrupt:
                print()
                return
        print("Too many invalid inputs, not switching template")
        return
