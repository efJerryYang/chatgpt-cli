# ChatGPT CLI

ChatGPT CLI is a command-line interface tool that connects to the ChatGPT language model using OpenAI's official API key. With markdown support, it allows you to structure your inputs in a readable and well-organized format for future reference.

Additionally, the tool saves conversations in JSON format and loads them when it starts.

We've provided serveral commands to help you use this tool more conveniently:

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

These commands are designed to enable you to use this tool much like you would use the official Web client. If you find that you need additinal command support, please feel free to open an issue.

Below is a simple demonstration of using this tool:

<!-- <insert gif> -->

## Usage

### Prequisites

To use ChatGPT CLI, you'll need to have `Python` installed on your machine. `Python` version `3.11.2` or later is supported, but older versions may work as well.

You'll also need an OpenAI API key (which you can [get here](https://platform.openai.com/account/api-keys)).

### Installation

To install ChatGPT CLI, simply clone this repository to your local machine:

```bash
git clone https://github.com/efJerryYang/chatgpt-cli.git
```

Then, navigate to the cloned repository and install the required dependencies:

```bash
pip install -r requirements.txt
```

To use this tool, you will need to have a `config.yaml` in the directory you place your script `chat.py`. Here is an example:

```yaml
# config.yaml.example
openai:
  api_key: <YOUR_API_KEY>
  default_prompt:
    - role: system
      content: You are ChatGPT, a language model trained by OpenAI. Now you are responsible for answering any questions the user asks.
proxy:
  http_proxy: http://127.0.0.1:7890
  https_proxy: http://127.0.0.1:7890
```

### Running the Tool

You should have the following directory structure:

```txt
.
|-- chat.py
|-- config.yaml
|-- config.yaml.example
|-- data
|   |-- example.json
|   `-- example2.json
|-- LICENSE
|-- README.md
`-- requirements.txt
```

The `data` directory should be created automatically the first time you run the script.

You can then run the following to start using this tool. And you can exit the tool by typing `!quit` command during your conversation, the script will prompt you to choose storing the conversation or not. (`quit` command in previous version is also supported till now)

```bash
python chat.py
```

To send a prompt to ChatGPT, simply hit the `[Enter]` key twice after your message. If you press `[Enter]` only once, it will create a new line, but if the message is blank, it will also be submitted to ChatGPT. Please note that if you submit an empty message, only the stripped empty string will be sent directly to ChatGPT without any prompts.

## Todos

- [ ] Detect `[Ctrl]+[C]` hotkey and prompt to confirm exiting
- [ ] Count tokens in conversation and display the total number
- [ ] Generate a summary of the conversation to reduce token usage

## Contributing

If you'd like to contribute to ChatGPT CLI, please feel free to submit a pull request or open an issue!

## References

- The idea of using the `rich.panel` package comes from [mbroton's chatgpt-api](https://github.com/mbroton/chatgpt-api).
<!-- - The !summarize command for generating a summary of the current conversation to guide the user in continuing the conversation is inspired by 沙漏/u202e. -->

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
