class Prompt:
    @classmethod
    def user(cls):
        print("\033[1;32mUSER:\033[0m\n> ", end="")
        return input()

    @classmethod
    def ai(cls, content):
        print(f"\033[1;31mAI:\033[0m\n{content}\n")
