import json
import requests

from src.client.console.prompt import Prompt


def command_parser(user_input):
    if user_input == "/exit":
        exit(0)
    elif user_input[0] == "/":
        user_input_arr = user_input.split(' ')
        command = user_input_arr[0][1:]
        args = {k.split('=')[0]: k.split('=')[1] for k in user_input_arr[1:]}
    else:
        command = "chat"
        args = {"message": user_input}
    return {"command": command, "args": json.dumps(args)}


def execute(command_with_args):
    result = requests.post('http://127.0.0.1:5000/command', data=command_with_args)
    return result


def loop():
    while True:
        user_input = Prompt.user()
        command = command_parser(user_input)
        content = execute(command)
        Prompt.ai(content.json()['response'])


if __name__ == "__main__":
    loop()
