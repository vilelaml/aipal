import openai
from src.server.memory.local import LocalMemory


class GptClient:
    MODEL = "gpt-3.5-turbo"
    ASSISTANT_ROLE = "assistant"
    USER_ROLE = "user"

    def __init__(self):
        self.memory = LocalMemory()

    def chat(self, message):
        self.memory.add_user_input(message)
        response = openai.ChatCompletion.create(model=self.MODEL, messages=self.memory.memories)
        content = response.choices[0].message.content
        self.memory.add(self.ASSISTANT_ROLE, content)
        return content

    def summarise(self):
        question = "Could you summarise our conversation?"
        self.memory.add(self.USER_ROLE, question)
        response = openai.ChatCompletion.create(model=self.MODEL, messages=self.memory.memories)
        content = response.choices[0].message.content
        self.memory.clear()
        self.memory.add(self.ASSISTANT_ROLE, content)
