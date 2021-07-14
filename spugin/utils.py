import string
from colorama import init as init_colorama
from colorama import Fore


class Utils:
    init_colorama()

    @staticmethod
    def create_jar_name(text: str) -> str:
        text = text.title()
        return text.translate(str.maketrans("", "", string.whitespace))

    @staticmethod
    def sanitise_input(text: str) -> str:
        # TODO: Probably need more here
        text.replace("/", "")
        text.replace("\\", "")
        return text

    @staticmethod
    def status(text):
        print(Fore.GREEN + text)

    @staticmethod
    def error(text):
        print(Fore.RED + text)

    @staticmethod
    def warning(text):
        print(Fore.YELLOW + text)

    @staticmethod
    def status_dict(status: bool, error_message: str = ""):
        return {
            "status": status,
            "error_message": error_message,
        }
