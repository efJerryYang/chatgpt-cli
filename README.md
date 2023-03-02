# ChatGPT CLI

ChatGPT CLI is a command-line interface tool that connects to the ChatGPT language model using OpenAI's official API key. With markdown support, it allows users to structure their inputs in a readable and well-organized format for future reference. Additionally, the tool saves conversations in JSON format and can be loaded when starting the tool.

## Usage

### Prequisites

To use ChatGPT CLI, you'll need to have `Python` installed on your machine. `Python` version over `3.11.2` is supported, and the older version may also work.

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
# config.yaml
openai:
  api_key: <your_openai_api_key>
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
|-- data
|   |-- example.json
|   `-- example2.json
|-- LICENSE
|-- README.md
`-- requirements.txt
```

The `data` directory should be created automatically the first time you run the script.

You can then run the following to start using this tool. And you can exit the tool by typing `quit` during your conversation, the script will prompt you to choose storing the conversation or not.

```bash
python chat.py
```

## Contributing

If you'd like to contribute to ChatGPT CLI, please feel free to submit a pull request or open an issue!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
