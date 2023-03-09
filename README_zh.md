# ChatGPT CLI

[![PyPI](https://img.shields.io/pypi/v/chatgpt-cli-md)](https://pypi.org/project/chatgpt-cli-md/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chatgpt-cli-md)](https://pypi.org/project/chatgpt-cli-md/) [![PyPI - License](https://img.shields.io/pypi/l/chatgpt-cli-md)](https://pypi.org/project/chatgpt-cli-md/) [![Stars](https://img.shields.io/github/stars/efJerryYang/chatgpt-cli)](https://github.com/efJerryYang/chatgpt-cli/stargazers)

[English](README.md)

## 简介

ChatGPT CLI 是一个使用 OpenAI 官方 API 和 ChatGPT 交互的命令行工具，支持 Markdown 语法的输入和输出，通过 `!show` 可以用 Markdown 渲染展示当前对话。

对话记录保存在 `JSON` 文件中，可以通过 `!load` 命令来载入历史对话。更多的命令使用可以通过 `!help` 命令来查看，或者参考[命令](#命令)部分

以下是一个简要的展示：

![demo](docs/demo/ezgif.com-optimize.gif)

<!-- For more detailed information, please check out the `<link_to_docs>`. -->

## 前置准备

运行 ChatGPT CLI 要求 Python 3.8 及以上版本，因为使用了 `importlib.metadata` 特性，但是这一特性在 3.8 及以后的版本才加入。可以通过在控制台运行 `python -V` 来查看当前环境的 Python 版本。

你同样需要一个 OpenAI 的 API key，可以从[官网](https://platform.openai.com/account/api-keys)获取。

可以使用 `pip install -r requirements.txt` 安装需要的包，包括：

- `openai >= 0.27.0`
- `pyyaml >= 6.0`
- `rich >= 13.3.1`

## 安装

可以从 [latest release](https://github.com/efJerryYang/chatgpt-cli/releases) 下载最新版本的包，运行以下两个命令之一进行安装。你需要注意的是，请将 `<version>` 替换为你下载的版本号，如 `0.1.0`。

你也可以选择执行 `pip install chatgpt-cli-md` 从 PyPI 安装。

```sh
pip install chatgpt-cli-md-<version>.tar.gz
```

```sh
pip install chatgpt_cli_md-<version>-py3-none-any.whl
```

这将自动安装所需的依赖，所以你需要确保你的网络连接没有问题。你也可以选择从源代码打包后安装，可以先 clone 当前项目：

```sh
git clone https://github.com/efJerryYang/chatgpt-cli.git
```

然后安装必要的依赖：

```sh
pip install -r requirements.txt
```

构建 Python 包：

```sh
python -m build
```

当构建完成之后，可以参考上文所给出的安装教程。你可以在 `dist` 目录下找到打包好的文件。

我们强烈建议你使用最新版本的 ChatGPT CLI，并且使用推荐的方法进行安装，以保证错误的修复和运行的稳定。

## 开始使用

在安装完成之后，你就可以通过在控制台执行 `chatgpt-cli` 来运行 ChatGPT CLI：

```sh
chatgpt-cli
```

如果你是第一次运行，将提示你配置 `config.yaml` 文件，以及选择是否导入之前版本 `data` 目录下的对话记录。 如果程序在 `${HOME}/.config/chatgpt-cli/config.yaml` 找不到配置文件，你可以选择根据交互提示新建一个，或者从原来 `config.yaml` 的路径导入。如果你选择新建一个，你需要根据提示输入你的 OpenAI API key，并且设置代理（如果你使用代理的话）。你可以从[这里](https://platform.openai.com/account/api-keys) 获取一个 OpenAI API key。

在配置完成之后，你会看到一个欢迎界面，目前只支持来英文显示，你可以正常使用中文和 ChatGPT 交流。欢迎界面也会呈现命令的帮助信息，此时你就已经可以开始和 ChatGPT 对话了。

## 命令

这些命令可以很方便的帮助我们使用这个命令行工具，因为这些都是以复刻 ChatGPT 的 web 端功能为目的编写的。你不需要记住太多，随时都可以通过 `!help` 进行查看。这些都是比较常用的命令：

- `!help` 呈现帮助信息，目前只有英文显示
- `!show` 用来呈现当前会话的所有消息（以 Markdown 渲染的格式）
- `!save` 保存当前会话到 `JSON` 文件
- `!load` 从文件加载会话，如果遇到当前会话未保存的情况，会提醒你是否选择保存当前会话。
- `!regen` 重新生成最后一次 ChatGPT 的回复
- `!new` 或者 `!reset` 重置会话，如果未保存的话会提示是否保存
- `!drop` 目前用于删除掉某一段消息，可以是 ChatGPT 的也可以是你发的
- `!resend` 通常用于在发送失败的情况下，如遇到网络错误，重新发送上一次的消息
- `!edit` 用于编辑会话，双方的话都可以编辑
- `!exit` 或者 `!quit` 退出，未保存的情况下也会提示是否保存

如果你需要新的命令来实现某个特定的功能，可以在这个仓库下开一个 issue，我根据我的时间安排会尽量完成的。

## Todos

We have some todos for future improvements, such as:

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
