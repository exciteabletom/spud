from __future__ import annotations

import json
import re
import string
import sys
from enum import Enum, unique
from typing import Union
import base64
import zipfile

import emoji
from colorama import Fore
from colorama import init as init_colorama

from . import settings
from .type import Plugin, Metadata


@unique
class Color(Enum):
    STATUS = Fore.LIGHTWHITE_EX
    SUCCESS = Fore.GREEN
    WARNING = Fore.YELLOW
    ERROR = Fore.RED


class Utils:
    init_colorama()

    @staticmethod
    def sanitise_api_plugin(plugin: Plugin) -> Plugin:
        """
        This method tries it's best to remove garbage from plugin names and tags.

        Example:
        "1.17 | Plugin Name - The Greatest Plugin in the universe!!!! 😂😂😂😂😂!!!! I lack humility!"

        becomes: "Plugin Name"

        :return: Plugin dict with BS removed
        """
        safe_chars: str = string.ascii_letters

        # Split plugin name by common separators
        split_name = re.split("[-|/!\\[\\]<>~•·×✘]", plugin["name"])
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

        plugin["tag"] = plugin["tag"].replace("|", "-")

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
    def format_text(text: str, ansi_color: Color, print_text=True) -> Union[str, None]:
        str_color: str = str(ansi_color.value)

        formatted_text = str_color + text + Fore.RESET
        if print_text:
            print(formatted_text)
            return None
        else:
            return formatted_text

    @classmethod
    def prompt(cls, text: str) -> str:
        try:
            return input(cls.format_text(text + ": ", Color.STATUS, print_text=False))
        except KeyboardInterrupt:
            sys.exit(1)

    @classmethod
    def prompt_bool(cls, question: str) -> bool:
        while True:
            try:
                answer = cls.prompt(question + " (y/n)").lower()
            except EOFError:
                return False

            if answer == "y":
                return True
            elif answer == "n":
                return False
            else:
                Utils.format_text("Answer must be 'y' or 'n'", Color.ERROR)

    @staticmethod
    def separator() -> None:
        sep_char = "="
        print(Fore.WHITE + (sep_char * 15) + Fore.RESET)

    @classmethod
    def inject_metadata_file(cls, plugin: Plugin, filename: str) -> None:
        # noinspection PyBroadException
        try:
            metadata: Metadata = {
                "search_name": plugin["name"],
                "plugin_id": plugin["id"],
                "plugin_version_id": plugin["version"]["id"],
            }

            metadata_json = json.dumps(metadata).encode("UTF-8")

            with zipfile.ZipFile(filename, "a") as jar:
                jar.writestr(settings.METADATA_FILENAME, metadata_json)
        except:
            cls.format_text(
                "Could not write metadata file due to an unknown error", Color.ERROR
            )

    @staticmethod
    def load_metadata_file(filename: str) -> Union[Metadata, None]:
        try:
            with zipfile.ZipFile(filename) as jar:
                metadata_str: str = jar.read(settings.METADATA_FILENAME).decode("UTF-8")

                tmp_metadata: dict = json.loads(metadata_str)

                # Validate that the keys in the metadata are of the correct type
                # to satisfy the type checker
                for key, value in Metadata.__annotations__.items():
                    if not type(tmp_metadata[key]) == value:
                        raise TypeError

                metadata: Metadata = {
                    "search_name": tmp_metadata["search_name"],
                    "plugin_id": tmp_metadata["plugin_id"],
                    "plugin_version_id": tmp_metadata["plugin_version_id"],
                }

                return metadata

        except (FileNotFoundError, KeyError, zipfile.BadZipfile):
            return None

    @staticmethod
    def split_title_case(text: str) -> str:
        return " ".join(re.findall(r"[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))", text))
