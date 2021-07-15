import json
import string
import sys
import zipfile

from colorama import init as init_colorama
from colorama import Fore

from . import settings


class Utils:
    init_colorama()

    @staticmethod
    def sanitise_input(text: str) -> str:
        # TODO
        return text

    @staticmethod
    def create_jar_name(text: str) -> str:
        text = Utils.sanitise_input(text)
        return text.translate(str.maketrans("", "", string.whitespace)) + ".jar"

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
    def status_dict(status: bool, message: str = ""):
        return {
            "status": status,
            "message": message,
        }

    # noinspection PyBroadException
    @staticmethod
    def inject_metadata_file(plugin: dict, filename: str) -> None:
        try:
            metadata = {
                "plugin_name": plugin.get("name"),
                "plugin_id": plugin.get("id"),
                "plugin_version_id": plugin.get("version").get("id"),
            }

            metadata = json.dumps(metadata).encode("UTF-8")

            with zipfile.ZipFile(filename, "a") as jar:
                jar.writestr(settings.METADATA_FILENAME, metadata)
        except:
            Utils.error("Could not write metadata file")

    # noinspection PyBroadException
    @staticmethod
    def load_metadata_file(filename: str) -> dict:
        try:
            with zipfile.ZipFile(filename) as jar:
                metadata: str = jar.read(settings.METADATA_FILENAME).decode("UTF-8")
                metadata: dict = json.loads(metadata)
                return metadata

        except (FileNotFoundError, KeyError):
            return {}
        except:
            Utils.error(f"Could not read metadata file due to unknown error.")
