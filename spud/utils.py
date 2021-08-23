import json
import re
import string
import sys
import zipfile

import emoji
from colorama import Fore
from colorama import init as init_colorama

from . import settings

colors = {
    "error": Fore.RED,
    "warning": Fore.YELLOW,
    "status": Fore.LIGHTWHITE_EX,
    "success": Fore.GREEN,
}


class StatusDict(dict):
    """
    A dict of form:
        {
            status: bool,
            message: str
        }
    """

    def __init__(self, status: bool, message: str = ""):
        super().__init__(status=status, message=message)


class Utils:
    init_colorama()

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
        # this should remove splits like (1.13-1.17) at the beginning of names
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
        return text.translate(str.maketrans("", "", string.whitespace)) + ".jar"

    @staticmethod
    def get_plugin_name_from_jar(jar_name: str) -> str:
        if jar_name.endswith(".jar"):
            return jar_name.replace(".jar", "")
        return jar_name

    @staticmethod
    def format_text(text: str, ansi_color: str, print_text=True) -> str or None:
        formatted_text = ansi_color + text + Fore.RESET
        if print_text:
            print(formatted_text)
        else:
            return formatted_text

    @classmethod
    def prompt(cls, text) -> str:
        try:
            return input(cls.format_text(text + ": ", colors["status"], print_text=False))
        except KeyboardInterrupt:
            sys.exit(1)

    @staticmethod
    def separator() -> None:
        sep_char = "="
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
            Utils.format_text(
                "Could not write metadata file due to an unknown error", colors["error"]
            )

    # noinspection PyBroadException
    @staticmethod
    def load_metadata_file(filename: str) -> dict or None:
        try:
            with zipfile.ZipFile(filename) as jar:
                metadata: str = jar.read(settings.METADATA_FILENAME).decode("UTF-8")
                metadata: dict = json.loads(metadata)
                return metadata

        except (FileNotFoundError, KeyError, zipfile.BadZipfile):
            return None

    @staticmethod
    def split_title_case(text: str) -> str:
        return " ".join(re.findall(r"[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))", text))
