# ChatGPT CLI

## Introduction

ChatGPT CLI is a command-line interface tool that connects to the ChatGPT language model using OpenAI's official API key. With markdown support, it allows you to structure your inputs in a readable and well-organized format for future reference. Additionally, the tool saves conversations in JSON format and loads them when it starts.

Here is a simple demonstration of how to use it:

![demo](demo/ezgif.com-optimize.gif)

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

## Prequisites

To use ChatGPT CLI, you'll need to have `Python>=3.8` installed on your machine. You can type `python -V` in your command line to see your python version, and the output of this command would look like this:

```sh
Python 3.11.2
```

You'll also need an OpenAI API key (which you can [get here](https://platform.openai.com/account/api-keys)).

The Python packages we used include `openai`, `pyyaml` and `rich`, which can be installed with `pip install -r requirements.txt`.

## Installation

To install ChatGPT CLI, simply clone this repository to your local machine:

```bash
git clone https://github.com/efJerryYang/chatgpt-cli.git
```

Then, navigate to the cloned repository and install the required dependencies:

```sh
pip install -r requirements.txt
```

To use this tool, you will need to have a `config.yaml` in the directory as your script `chat.py`. You can copy the content of `config.yaml.example` and repalce the api key placeholder with your own OpenAi API key.

If you're running the tool over a proxy, replace the `http://127.0.0.1:7890` with the address and port of your proxy server in the `http_proxy` and `https_proxy` fields respectively. If you're not using a proxy or you're not sure what to set these fields to, you can ignore the `proxy` field or delete it from your `config.yaml` file. Here is an example of a `config.yaml` file with a proxy:

```yaml
# config.yaml.example
openai:
  api_key: <YOUR_API_KEY>
  default_prompt:
    - role: system
      content: You are ChatGPT, a language model trained by OpenAI. Now you are responsible for answering any questions the user asks.
proxy:
  http_proxy: http://yourproxyserver.com:8080
  https_proxy: http://yourproxyserver.com:8080
```

Remember to replace `http://yourproxyserver.com:8080` with the address and port of your proxy server. If you don't want to use a proxy, you can delete the `proxy` field from your `config.yaml` file, like this:

```yaml
# config.yaml.example
openai:
  api_key: <YOUR_API_KEY>
  default_prompt:
    - role: system
      content: You are ChatGPT, a language model trained by OpenAI. Now you are responsible for answering any questions the user asks.
# no proxy field is okay to run this tool
```

## Running the Tool

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

`chat.py` is the script to run, and `config.yaml` is the configuration file that sets up the runtime environment. The `data` directory should be created automatically the first time you run the script after you have installed the required dependencies.

To start using this tool, run the following command:

```sh
python chat.py
```

You can exit the tool by typing `!quit` command during your conversation, and the script will prompt you to choose storing the conversation or not once you make changes to current conversation. The `quit` command in previous versions is also supported.

To send a prompt to ChatGPT, hit the `[Enter]` key twice after your message. If you press `[Enter]` only once, it will create a new line, but if the message is blank, it will also be submitted to ChatGPT. Note that if you submit an empty message, only the stripped empty string will be sent directly to ChatGPT without any prompts.

## Using this tool as a binary (Optional)

It would be more convenient if the script could be run from any directory, but unfortunately I'm not familiar with packaging Python projects for PyPI.

Alternatively, the following commands can help run it as a binary, you can save the command you use as `sync_bin.sh` or `sync_bin.bat` so that it would not be tracked by `git` (see `.gitignore`), and which name you use depends on the OS type.

### Unix-like OS users

1. First, create a directory named `bin` if it does not exist in the root directory of the project:

   ```sh
   mkdir bin
   ```

2. Then, copy the `chat.py` file to the `bin` directory and rename it to `chatgpt-cli`:

   ```sh
   cp -a chat.py bin/chatgpt-cli
   ```

3. Modify the shebang line of the `chatgpt-cli` file to use the path of your Python interpreter that installed the `requirements.txt`.

   ```sh
   sed -i '1i\#!/path/to/your/requirements/installed/python' bin/chatgpt-cli
   ```

   > _Note: Replace `/path/to/your/requirements/installed/python` with the actual path to your Python interpreter that has the required packages installed. For example, in my case it would be: `/home/jerry/.pyenv/versions/3.11.2/envs/openai-utils/bin/python`_

4. Finally, set the execute permission for the `chatgpt-cli` file if it does not have currently:

   ```sh
   sudo chmod a+x bin/chatgpt-cli
   ```

5. Add the following line to your shell run command file, such as `.bashrc`, to include the `bin` directory to your `$PATH` environment variable:

   ```sh
   # chatgpt-cli here is the project directory name
   export PATH=${PATH}:/absolute/path/to/your/chatgpt-cli/bin
   ```

6. Type `source ~/.bashrc` (or a similar command) to start using this tool from any directory.

Now, you can run the `chatgpt-cli` command from any terminal or command prompt window, regardless of your current working directory.

### Windows Users

> _Notice that the following content for windows users is generated by ChatGPT, it might not be reliable currently. However, now I am not very convenient to test the steps below on a windows machine. If you find any mistakes below, please let me know._

1. Create a directory named bin in the root directory of the project.
2. Copy the `chat.py` file to the bin directory and rename it to `chatgpt-cli.py`.
3. Open the environment variable settings window by searching for "Environment Variables" in the Windows search bar.
4. Click on "Edit the system environment variables" and then click on the "Environment Variables" button.
5. In the "User variables" or "System variables" section, find the PATH variable, and click on the "Edit" button.
6. In the "Edit environment variable" window, click on the "New" button and add the absolute path to the bin directory (e.g., `C:\Projects\chatgpt-cli\bin`). Click on "OK" to close all the windows.
7. In the bin directory, create a new file named `chatgpt-cli.bat` and paste the following contents:

   ```bat
   @echo off
   python "%~dp0\chatgpt-cli.py" %*
   ```

8. Save the file and close it.
9. Open a new command prompt or PowerShell window and run the `chatgpt-cli` command.

Now, you can run the `chatgpt-cli` command from any terminal or command prompt window, regardless of your current working directory.

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
