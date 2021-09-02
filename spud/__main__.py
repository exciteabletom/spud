"""
Main module for running the CLI abstraction to the API backend

classes:
    Main - Represents a CLI interface

Functions:
    init - Initialises a new CLI instance
"""
from __future__ import annotations

from argparse import ArgumentParser, Namespace
import os
from pathlib import Path
from typing import Collection, Union

from . import api
from .utils import Utils, Color
from .type import StatusDict, Plugin, Metadata, Update
from .settings import VERSION


class Main:
    """Class for handling program arguments and providing a user interface for the API backend"""

    def __init__(self, api_class=api.SpigetAPI) -> None:
        """Initialise the cli application"""
        self.api = api_class()

        self.args: Namespace = self.parse_args()

        os.chdir(self.args.directory)

        if self.args.action == "install":
            self.install(self.args.plugins)
        elif self.args.action == "update":
            self.update(self.args.plugins)
        else:
            Utils.format_text(f"Action {self.args.action} does not exist", Color.ERROR)

    def install(self, plugins: Collection[str]) -> None:
        """
        Download the jars for a list of plugins and save them as files.

        :param plugins: A list of plugin names or jar filenames
        """
        for plugin_name in plugins:
            plugin_name = Utils.get_plugin_name_from_jar(plugin_name)

            plugin_list = self.api.search_plugins(plugin_name)

            if not plugin_list:
                Utils.format_text(
                    f"No plugin with name {plugin_name} found.", Color.ERROR
                )
                continue

            Utils.format_text(f"Query: {plugin_name}", Color.SUCCESS)

            if self.args.noninteractive:
                plugin = plugin_list[0]
            else:
                plugin = self.get_plugin_choice(plugin_list)

            if not plugin:
                Utils.format_text("Skipping Install!", Color.ERROR)
                continue

            Utils.format_text(f"Installing {plugin['name']}", Color.STATUS)

            result: StatusDict = self.api.download_plugin(plugin)

            if result["status"]:
                Utils.format_text(
                    f"{plugin['name']} was installed successfully",
                    Color.SUCCESS,
                )
            else:
                Utils.format_text(result["message"], Color.WARNING)

    def update(self, plugins: Collection[str]) -> None:
        """
        Check if plugins need updates, and if they do update them.

        :param plugins: An list of plugin names or jar filenames
        """
        if not plugins:
            file_list = os.listdir()
            plugins = [i for i in file_list if i.endswith(".jar")]
            Utils.format_text(
                f"Detected {len(plugins)} plugins in {os.getcwd()}", Color.STATUS
            )

        update_count = 0
        for plugin_name in plugins:
            filename = plugin_name
            if ".jar" not in filename:
                filename = Utils.create_jar_name(plugin_name)

            metadata: Union[Metadata, None] = Utils.load_metadata_file(filename)

            if not metadata:
                Utils.format_text(
                    f"Couldn't load metadata for {filename}. Try reinstalling with spud first",
                    Color.WARNING,
                )
                continue

            plugin: Union[Plugin, None] = self.api.get_plugin_info_if_update(metadata)
            if plugin is None:
                continue

            result = {}

            if not self.args.noninteractive:
                update: Update = self.api.get_latest_update_info(plugin)
                changelog = update["description"]
                Utils.separator()
                Utils.format_text(f"Changelog for {plugin['name']}:", Color.STATUS)
                Utils.format_text(changelog, Color.STATUS)
                Utils.separator()

                if not Utils.prompt_bool(f"Would you like to update {plugin['name']}?"):
                    result = {
                        "status": False,
                        "message": f"Not updating {plugin['name']}",
                    }

            if not result:
                result = self.api.download_plugin(plugin, filename)

            color = Color.WARNING
            if result["status"]:
                update_count += 1
                color = Color.SUCCESS

            if message := result["message"]:
                Utils.format_text(message, color)

        Utils.separator()
        Utils.format_text(
            f"{update_count} updated, {len(plugins) - update_count} left unchanged",
            Color.STATUS,
        )

    @staticmethod
    def parse_args() -> Namespace:
        """
        :return: a Namespace instance for the program's arguments
        """
        parser = ArgumentParser(
            description="Spud: The plugin manager for your Spigot Minecraft server",
            epilog="Licensed under GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html). "
            "Source available at https://github.com/exciteabletom/spud",
        )
        parser.add_argument("action", help="install or update", type=str)
        parser.add_argument(
            "plugins",
            metavar="name",
            help="the names (or filenames) of plugins",
            type=str,
            nargs="*",
        )
        parser.add_argument(
            "-n",
            dest="noninteractive",
            help="run without asking for input",
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "-d",
            "--directory",
            dest="directory",
            help="path to plugins directory, defaults to the working directory",
            type=Path,
            default=".",
        )
        parser.add_argument(
            "-v", "--version", action="version", version=f"%(prog)s {VERSION}"
        )
        return parser.parse_args()

    @staticmethod
    def get_plugin_choice(plugin_list: list[Plugin]) -> Union[Plugin, None]:
        """
        Gets a user's choice out of a list of plugins

        :returns: The Plugin dict the user chose, or None if they didn't choose one
        """
        Utils.separator()
        for index, plugin in enumerate(plugin_list):
            Utils.format_text(
                f"{index} | {plugin['name']} by {plugin['author']['name']} | {plugin['tag']}",
                Color.STATUS,
            )

        Utils.separator()
        while True:
            try:
                chosen_id: int = int(
                    Utils.prompt("Select a plugin ID (Ctrl-D to skip)")
                )
            except ValueError:
                continue
            except EOFError:
                return None

            if 0 <= chosen_id < len(plugin_list):
                return plugin_list[chosen_id]

            continue


def init():
    """Mainline function called when app starts"""
    Main()
