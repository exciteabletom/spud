import argparse
import os
from pathlib import Path

from . import api
from .utils import Utils, StatusDict, colors


class Main:
    """
    Class for handling program arguments and providing a user interface for the API backend
    """

    def __init__(self, api_class):
        """Initialise a new cli application"""
        self.spiget_api = api_class()

        self.args = self.parse_args()

        os.chdir(self.args.directory)

        if self.args.action == "install":
            self.install(self.args.plugins)
        elif self.args.action == "update":
            self.update(self.args.plugins)
        else:
            Utils.format_text(
                f"Action {self.args.action} does not exist", colors["error"]
            )

    def install(self, plugins):
        for plugin_name in plugins:
            plugin_name = Utils.get_plugin_name_from_jar(plugin_name)

            plugin_list = self.spiget_api.search_plugins(plugin_name)

            if not plugin_list:
                Utils.format_text(
                    f"No plugin with name {plugin_name} found.", colors["error"]
                )
                continue

            Utils.format_text(f"Query: {plugin_name}", colors["success"])

            if self.args.noninteractive:
                plugin = plugin_list[0]
            else:
                plugin = self.get_plugin_choice(plugin_list)

            if not plugin:
                Utils.format_text("Skipping!", colors["warning"])
                continue

            Utils.format_text(f"Installing {plugin.get('name')}", colors["status"])

            result: dict = self.spiget_api.download_plugin(plugin)

            if result.get("status"):
                Utils.format_text(
                    f"{plugin.get('name')} was installed successfully",
                    colors["success"],
                )
            else:
                Utils.format_text(result.get("message"), colors["warning"])
        pass

    def update(self, plugins):
        if not plugins:
            file_list = os.listdir()
            plugins = [i for i in file_list if i.endswith(".jar")]
            Utils.format_text(
                f"Detected {len(plugins)} plugins in {os.getcwd()}", colors["status"]
            )

        update_count = 0
        for plugin_name in plugins:
            filename = plugin_name
            if ".jar" not in filename:
                filename = Utils.create_jar_name(plugin_name)

            result: StatusDict = self.spiget_api.download_plugin_if_update(filename)

            if result.get("status"):
                update_count += 1
                color = colors["success"]
            else:
                color = colors["warning"]

            if message := result.get("message"):
                Utils.format_text(message, color)

        Utils.separator()
        Utils.format_text(
            f"{update_count} updated, {len(plugins) - update_count} left unchanged",
            colors["status"],
        )

    @staticmethod
    def parse_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            description="Spud: The plugin manager for your Spigot Minecraft server",
            epilog="Licensed under GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)",
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
        return parser.parse_args()

    @staticmethod
    def get_plugin_choice(plugin_list: list) -> dict or None:
        Utils.separator()
        for index, plugin in enumerate(plugin_list):
            Utils.format_text(
                f"{index} | {plugin.get('name')} by {plugin.get('author').get('name')} | {plugin.get('tag')}",
                colors["status"],
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
            else:
                continue


def init():
    Main(api.SpigetAPI)
