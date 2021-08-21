import argparse
import os
from pathlib import Path

from . import api
from .utils import Utils


class Main:
    def __init__(self, api_instance):
        self.spiget_api: api.SpigetAPI = api_instance

    @staticmethod
    def parse_args():
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
        args = parser.parse_args()
        return args

    @staticmethod
    def get_plugin_choice(plugin_list: list) -> dict or None:
        Utils.separator()
        for index, plugin in enumerate(plugin_list):
            Utils.status(
                f"{index} | {plugin.get('name')} by {plugin.get('author').get('name')} | {plugin.get('tag')}"
            )

        Utils.separator()

        while True:
            try:
                chosen_ID: int = int(
                    Utils.prompt("Select a plugin ID (Ctrl-D to skip)")
                )
            except ValueError:
                continue
            except EOFError:
                return None

            if 0 <= chosen_ID < len(plugin_list):
                return plugin_list[chosen_ID]
            else:
                continue

    def main(self):
        args = self.parse_args()
        os.chdir(args.directory)

        if args.action == "install":
            for plugin_name in args.plugins:
                plugin_name = Utils.get_plugin_name_from_jar(plugin_name)

                plugin_list = self.spiget_api.search_plugins(plugin_name)

                if not plugin_list:
                    Utils.error(
                        f"No plugin with name {plugin_name} found.", fatal=False
                    )
                    continue

                Utils.status_good(f"Query: {plugin_name}")

                if args.noninteractive:
                    plugin = plugin_list[0]
                else:
                    plugin = self.get_plugin_choice(plugin_list)

                if not plugin:
                    Utils.warning("Skipping!")
                    continue

                Utils.status(f"Installing {plugin.get('name')}")

                result: dict = self.spiget_api.download_plugin(plugin)

                if result.get("status"):
                    Utils.status(f"{plugin.get('name')} was installed successfully")
                else:
                    Utils.warning(result.get("message"))

        elif args.action == "update":
            if not args.plugins:
                args.plugins = os.listdir()
                plugins = [i for i in args.plugins if i.endswith(".jar")]
            else:
                plugins = args.plugins

            for plugin_name in plugins:
                filename = plugin_name
                if ".jar" not in filename:
                    filename = Utils.create_jar_name(plugin_name)

                result = self.spiget_api.download_plugin_if_update(filename)

                if result.get("status"):
                    Utils.status(result.get("message"))
                else:
                    Utils.warning(result.get("message"))

        else:
            Utils.error(f"Action {args.action} does not exist")


def init():
    Main(api.SpigetAPI()).main()
