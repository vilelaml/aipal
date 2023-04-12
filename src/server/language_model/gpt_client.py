import openai

from src.server.config.config import Config


class GptClient:
    MODEL = "gpt-3.5-turbo"

    def __init__(self):
        self.memory = Config().memory

    def chat(self, message):
        messages = [self._prepare_message(m) for m in self.memory.get_relevant(message)]
        self.memory.add(message)
        messages.append(self._prepare_message(message))
        response = openai.ChatCompletion.create(model=self.MODEL, messages=messages)
        content = response.choices[0].message.content
        self.memory.add(content)
        return content

    def summarise(self):
        question = "Could you summarise our conversation?"
        self.memory.add(question)
        response = openai.ChatCompletion.create(model=self.MODEL, messages=self.memory.memories)
        content = response.choices[0].message.content
        self.memory.clear()
        self.memory.add(content)

    def _prepare_message(self, message: str) -> dict[str, str]:
        return {"role": "user", "content": message}
