import string
import sys
from colorama import init as init_colorama
from colorama import Fore


class Utils:
    init_colorama()

    @staticmethod
    def sanitise_input(text: str) -> str:
        # TODO: Probably need more here
        text.replace("/", "")
        text.replace("\\", "")
        return text

    @staticmethod
    def create_jar_name(text: str) -> str:
        text = Utils.sanitise_input(text)
        return text.translate(str.maketrans("", "", string.whitespace))

    @staticmethod
    def status(text):
        print(Fore.GREEN + text + Fore.RESET)

    @staticmethod
    def error(text, do_exit=True):
        print(Fore.RED + text + Fore.RESET)
        if do_exit:
            sys.exit(1)

    @staticmethod
    def warning(text):
        print(Fore.YELLOW + text + Fore.RESET)

    @staticmethod
    def prompt(text):
        return input(Fore.CYAN + text + ": " + Fore.RESET)

    @staticmethod
    def status_dict(status: bool, error_message: str = ""):
        return {
            "status": status,
            "error_message": error_message,
        }
