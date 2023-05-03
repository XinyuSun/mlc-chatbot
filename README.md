# Python Interface for MLC CHAT CLI

This simple code allows you to interact with the MLC LLM using the official CLI (command-line interface) app using python api.

## Install
***First of all***, You should install `MLC LLM` follwing official [instruction](https://mlc.ai/mlc-llm/), and are able to run `mlc_chat_cli` in the terminal. After that, you can feel free to copy this python code to your project or directly install by running:
```bash
python setup.py install
```

## Usage
This code provide several python api to interact with MLC LLM, take string as input and get response string. It is recommand to run this code under the mlc-llm root with a `dist` folder that contains libary files. Or you can specify the path of `dist` folder manually.


```python
>>> from mlc_chatbot import ChatBot
>>> bot = ChatBot()
"""
you can also specify the folder of the library and executable path by:
>>> bot = ChatBot(dist_url='{PATH_TO_DIST}', cli_dir='{PATH_TO_CLI}')
for example, a Windows user:
>>> bot = ChatBot(dist_url='~/mlc-chat/dist', cli_dir='~/miniconda3/envs/mlc-chat/Library/bin/mlc_chat_cli.exe')
"""
# now chat with mlc llm using python interface!
>>> bot.send('hello!')
>>> 'Hello! How can I help you today?'
# restart a fresh chat 
>>> bot.reset()
# get status of llm
>>> bot.status()
# encode speed and decode speed (token/s)
>>> (39.4, 26.0)
```