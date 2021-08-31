"""
Miscellaneous utilities

Classes:
    Color - An Enum of ansi colors
    Utils - General utilities
"""
from __future__ import annotations

import json
import re
import string
import sys
from enum import Enum, unique
from typing import Union, get_type_hints
import zipfile

import colorama
import emoji
from colorama import Fore, Style, Back
from colorama import init as init_colorama

from . import settings
from .type import Plugin, Metadata


@unique
class Color(Enum):
    """Enum of several ANSI colors labelled by use case"""

    STATUS = Style.BRIGHT + Fore.WHITE
    DIMMED = Style.NORMAL + Fore.WHITE
    SUCCESS = Fore.GREEN
    WARNING = Fore.YELLOW
    ERROR = Fore.RED


# Static class
class Utils:
    """
    A static class of methods which perform basic, general tasks.
    This class shouldn't be initialised before use.
    """

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
        """Remove whitespace and append '.jar'"""
        return text.translate(str.maketrans("", "", string.whitespace)) + ".jar"

    @staticmethod
    def get_plugin_name_from_jar(jar_name: str) -> str:
        """Remove '.jar' from the end of the string"""
        if jar_name.endswith(".jar"):
            return jar_name.replace(".jar", "")
        return jar_name

    @staticmethod
    def format_text(text: str, ansi_color: Color, print_text=True) -> Union[str, None]:
        """
        Format text with a color

        :param text: The text to print
        :param ansi_color: The Ansi color to use
        :param print_text: Whether to print the text or return it, default: True
        """
        str_color: str = str(ansi_color.value)

        formatted_text = str_color + text + Style.RESET_ALL
        if print_text:
            print(formatted_text)
            return None

        return formatted_text

    @classmethod
    def prompt(cls, question: str) -> str:
        """Prompt the user for an arbitrary string input."""
        try:
            return input(
                cls.format_text(question + ": ", Color.WARNING, print_text=False)
            )
        except KeyboardInterrupt:
            sys.exit(1)

    @classmethod
    def prompt_bool(cls, question: str) -> bool:
        """Ask the user a yes/no question and return a boolean"""
        while True:
            try:
                answer = cls.prompt(question + " (y/n)").lower()
            except EOFError:
                return False

            if answer == "y":
                return True
            if answer == "n":
                return False

            Utils.format_text("Answer must be 'y' or 'n'", Color.ERROR)

    @staticmethod
    def separator() -> None:
        """Print 20 * '-'"""
        sep_char = "-"
        Utils.format_text(sep_char * 20, Color.DIMMED)

    @classmethod
    def inject_metadata_file(cls, plugin: Plugin, filename: str) -> None:
        """Insert a Plugin's metadata into a filename"""
        metadata: Metadata = {
            "search_name": plugin["name"],
            "plugin_id": plugin["id"],
            "plugin_version_id": plugin["version"]["id"],
        }

        metadata_json = json.dumps(metadata).encode("UTF-8")

        with zipfile.ZipFile(filename, "a") as jar:
            jar.writestr(settings.METADATA_FILENAME, metadata_json)

    @staticmethod
    def load_metadata_file(filename: str) -> Union[Metadata, None]:
        """
        Load a metadata file from a Plugin jar

        :param filename: The filename to get the metadata from
        :returns: Metadata dict, or None if the file was invalid
        """
        try:
            with zipfile.ZipFile(filename) as jar:
                metadata_str: str = jar.read(settings.METADATA_FILENAME).decode("UTF-8")

                tmp_metadata: dict = json.loads(metadata_str)

                # Validate that the keys in the metadata are of the correct type
                # to satisfy the type checker
                for key, value in get_type_hints(Metadata).items():
                    if not isinstance(tmp_metadata[key], value):
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
        """Split a title case word up with spaces. E.g. 'FooBar' -> 'Foo Bar'"""
        return " ".join(re.findall(r"[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))", text))
