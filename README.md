# ChatGPT CLI

## Introduction

ChatGPT CLI is a command-line interface tool that connects to the ChatGPT language model using OpenAI's official API key. With markdown support, it allows you to structure your inputs in a readable and well-organized format for future reference. Additionally, the tool saves conversations in JSON format and loads them when it starts.

Here is a simple demonstration of how to use it:

![demo](docs/demo/ezgif.com-optimize.gif)

You can refer to the `<link_to_docs>` for more details.

## Prequisites

- `Python >= 3.8`

You can type `python -V` in your terminal to see your python version. We restrict the python version to 3.8 because the feature of `importlib.metadata` is added only after this version.

You'll also need an OpenAI API key (which you can [get here](https://platform.openai.com/account/api-keys)).

Python packages we used can be installed with `pip install -r requirements.txt`, which include the following:

- `openai >= 0.27.0`
- `pyyaml >= 6.0`
- `rich >= 13.3.1`

## Installation

To be compatible with previous script version, we support the running script version as well as the newly updated python package installation.

### Install from Release

You can install the packages from release by:

```sh
pip install chatgpt-cli-0.1.0.tar.gz
```

Or:

```sh
pip install chatgpt_cli-1.0.0-py3-none-any.whl
```

All the dependencies needed for running this tool will be installed automatically.

### Build and Install

You can also build this project and get the binary to install by running the following:

First, you can clone the project by running the following:

```sh
git clone https://github.com/efJerryYang/chatgpt-cli.git
```

Then, navigate to the cloned repository and install the required dependencies:

```sh
pip install -r requirements.txt
```

Next, build the project into package, the package files `*.tar.gz` or `*.whl` will be exported to `dist/` directory.

```sh
python -m build
```

Then you can following the instructions above to install the package.

### Run the Script Version

If you are still interested in running it using script, you can navigate to the `script/` directory, and do whatever the same as original version. Currently, you can refer to the [Old README](docs/archive/README.md) for its usage.

However, this is not recommended and the script there will not be maintained actively. Changes like bugfixes or new features will not be applied to the script simultaneously.

Moreover, it is rather easy to convert from old script version to current version by importing old `config.yaml` and data directory using the updated `chatgpt-cli` tool.

## Running the Tool

Once you have the package installed through `pip` command, you will be able to access this tool by typing `chatgpt-cli` in your terminal.

```sh
chatgpt-cli
```

Then, you will be prompted to setup the `config.yaml` if you do not currently have one in the path `${HOME}/.config/chatgpt-cli/config.yaml`. You can also import the data directory from your previous script version, and the new data directory will be at `${HOME}/.config/chatgpt-cli/data/`.

If you have not installed this tool on your machine, you can create a new `config.yaml` with the interactive setup procedure provided by the tool. You will be prompted to input your OpenAI's API key, and proxy settings (if you have one). If you don't currently have an OpenAI's API key, you can [get one here](https://platform.openai.com/account/api-keys).

Once you have setup all the configuration, you will be displayed with a welcome panel with help information, and you can then start chatting to ChatGPT!

## Commands

We've provided serveral commands to help you use this tool more conveniently. You don't need to remember all of them to start, as you can type `!help` whenever you want to have a look:

- `!help`: shows the help message
- `!show`: displays the current conversation messages
- `!save`: saves the current conversation to a `JSON` file
- `!load`: loads a conversation from a `JSON` file
- `!new` or `!reset`: starts a new conversation
- `!regen`: regenerates the last response
- `!resend`: resends your last prompt to generate response
- `!edit`: selects messages for editing
- `!drop`: selects messages for deletion
- `!exit` or `!quit`: exits the program

These commands are designed to enable you to use this tool much like you would use the official web client. If you find that you need additinal command support, feel free to open an issue.

## Todos

- [ ] Detect `[Ctrl]+[C]` hotkey and prompt to confirm exiting
- [ ] Fix inconsistent operation for `!edit` and `!drop`
- [ ] `!token`: Count tokens in conversation and display the total number
- [ ] `!sum`: Generate a summary of the conversation to reduce token usage
- [ ] `!tmpl`: Choose system prompt templates
- [ ] `!conv`: Show conversation list, Delete and Rename saved conversations
- [ ] `!sys <command>`: Enable you to run system command

## Contributing

If you'd like to contribute to ChatGPT CLI, please feel free to submit a pull request or open an issue!

## References

- The idea of using the `rich.panel` package comes from [mbroton's chatgpt-api](https://github.com/mbroton/chatgpt-api).
- The `!sum` command for generating a summary of the current conversation to guide the user in continuing the conversation is inspired by 沙漏/u202e.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
