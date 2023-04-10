from src.chat_client import ChatClient
from src.server.command import Command
from src.memory import Memory
from src.ui import Ui


if __name__ == "__main__":
    memory = Memory()
    client = ChatClient()
    while True:
        user_input = Ui.user_prompt()
        if Command.parse_input(user_input):
            response = client.chat(user_input)
            Ui.ai_prompt(response)
