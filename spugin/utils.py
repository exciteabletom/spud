import string
import sys
from colorama import init as init_colorama
from colorama import Fore


class Utils:
    init_colorama()

    @staticmethod
    def create_jar_name(text: str) -> str:
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
    def error(text, do_exit=True):
        print(Fore.RED + text)
        if do_exit:
            sys.exit(1)

    @staticmethod
    def warning(text):
        print(Fore.YELLOW + text)

    @staticmethod
    def prompt(text):
        return input(Fore.CYAN + text + ": ")

    @staticmethod
    def status_dict(status: bool, error_message: str = ""):
        return {
            "status": status,
            "error_message": error_message,
        }
