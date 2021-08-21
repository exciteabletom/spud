import json
import re
import string
import sys
import zipfile

import emoji
from colorama import Fore
from colorama import init as init_colorama

from . import settings


class StatusDict(dict):
    """
    A dict of form:
        {
            status: bool,
            message: str
        }
    """

    def __init__(self, status, message=""):
        super().__init__()
        self["status"] = status
        self["message"] = message


class Utils:
    init_colorama()

    @staticmethod
    def sanitise_input(text: str) -> str:
        # TODO: Is this needed?
        return text

    @staticmethod
    def sanitise_api_plugin(plugin: dict) -> dict:
        """
        This method tries it's best to remove garbage from plugin names and tags.

        Example:
        "1.17 | Plugin Name - The Greatest Plugin in the universe!!!! 😂😂😂😂😂!!!! I lack humility!"

        becomes: "Plugin Name"

        :return: Plugin dict with name and tag value sanitised from BS
        """
        safe_chars = string.ascii_letters

        # Split plugin name by common separators
        split_name = re.split("[-|/!\\[\\]<>~•·×✘]", plugin.get("name"))
        name = ""
        # If a split doesn't contain any safe characters we can assume it is fluff
        # this should remove segments like (1.13-1.17) at the beginning of names
        for split in split_name:
            for char in split:
                if char in safe_chars:
                    name += split + "|"
                    break

        for index, char in enumerate(name):
            if char in "|":
                name = name[:index]

        # Remove all emojis from name
        name = emoji.get_emoji_regexp().sub("", name)

        # Remove leading and trailing whitespace
        plugin["name"] = name.strip()

        plugin["tag"] = plugin.get("tag").replace("|", "-")

        return plugin

    @staticmethod
    def create_jar_name(text: str) -> str:
        text = Utils.sanitise_input(text)
        return text.translate(str.maketrans("", "", string.whitespace)) + ".jar"

    @staticmethod
    def get_plugin_name_from_jar(jar_name: str) -> str:
        if jar_name.endswith(".jar"):
            return jar_name.replace(".jar", "")
        return jar_name

    @staticmethod
    def status(text) -> None:
        print(Fore.LIGHTWHITE_EX + text + Fore.RESET)

    @staticmethod
    def status_good(text) -> None:
        print(Fore.GREEN + text + Fore.RESET)

    @staticmethod
    def error(text, fatal=True) -> None:
        print(Fore.RED + text + Fore.RESET)
        if fatal:
            sys.exit(1)

    @staticmethod
    def warning(text) -> None:
        print(Fore.YELLOW + text + Fore.RESET)

    @staticmethod
    def prompt(text) -> str:
        try:
            return input(Fore.CYAN + text + ": " + Fore.RESET)
        except KeyboardInterrupt:
            sys.exit(1)

    @staticmethod
    def separator() -> None:
        sep_char = "-"
        print(Fore.WHITE + (sep_char * 15) + Fore.RESET)

    # noinspection PyBroadException
    @staticmethod
    def inject_metadata_file(plugin: dict, filename: str) -> None:
        try:
            metadata = {
                "search_name": plugin.get("name"),
                "plugin_id": plugin.get("id"),
                "plugin_version_id": plugin.get("version").get("id"),
            }

            metadata = json.dumps(metadata).encode("UTF-8")

            with zipfile.ZipFile(filename, "a") as jar:
                jar.writestr(settings.METADATA_FILENAME, metadata)
        except:
            Utils.error("Could not write metadata file due to an unknown error!")

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

    @staticmethod
    def split_title_case(text: str) -> str:
        return " ".join(re.findall(r"[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))", text))
