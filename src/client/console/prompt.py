class Prompt:
    @classmethod
    def user(cls):
        print("\t\033[1;32mUSER:\033[0m\n\t\t", end="")
        return input()

    @classmethod
    def ai(cls, content):
        print(f"\t\033[1;31mAI:\033[0m\n\t\t{content}\n")
