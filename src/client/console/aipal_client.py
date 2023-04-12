import json
import requests

from src.client.console.prompt import Prompt

AI_PAL_URL = 'http://127.0.0.1:5000/command'


def command_parser(user_input):
    if user_input == "/exit":
        exit(0)
    elif user_input == "/help":
        for command in show_commands():
            print(f"/{command}")
        return
    elif user_input[0] == "/":
        user_input_arr = user_input.split(' ')
        command = user_input_arr[0][1:]
        args = {k.split('=')[0]: k.split('=')[1] for k in user_input_arr[1:]}
        return {"command": command, "args": json.dumps(args)}
    else:
        command = "chat"
        args = {"message": user_input}
        return {"command": command, "args": json.dumps(args)}


def execute(command_with_args):
    result = requests.post(AI_PAL_URL, data=command_with_args)
    return result


def show_commands():
    result = requests.get(AI_PAL_URL)
    return result.json()['commands']


def loop():
    while True:
        user_input = Prompt.user()
        command = command_parser(user_input)
        if command:
            content = execute(command)
            Prompt.ai(content.json()['response'])


if __name__ == "__main__":
    loop()
