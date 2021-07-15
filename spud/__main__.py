import argparse
import os

from pathlib import Path
from . import api
from .utils import Utils


def parse_args():
    parser = argparse.ArgumentParser(
        description="Spud: The plugin manager for your Spigot Minecraft server"
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
        "-d",
        "--directory",
        dest="directory",
        help="path to plugins directory, defaults to `.`",
        type=Path,
        default=".",
    )
    args = parser.parse_args()
    return args


def get_plugin_choice(plugin_list: list) -> dict:
    Utils.status("--------------------")
    for index, plugin in enumerate(plugin_list):
        Utils.status(f"{index} | {plugin.get('name')} | {plugin.get('tag')}")
    Utils.status("--------------------")

    while True:
        try:
            chosen_ID: int = int(Utils.prompt("Select a plugin ID"))
        except ValueError:
            continue

        if 0 <= chosen_ID < len(plugin_list):
            return plugin_list[chosen_ID]
        else:
            continue


def main():
    args = parse_args()
    os.chdir(args.directory)

    spiget_api = api.SpigetAPI()
    if args.action == "install":
        for plugin_name in args.plugins:
            plugin_name = Utils.get_plugin_name_from_jar(plugin_name)

            plugin_list = spiget_api.search_plugins(plugin_name)
            plugin = get_plugin_choice(plugin_list)

            Utils.status(f"Installing {plugin.get('name')}")

            result: dict = spiget_api.download_plugin(plugin)

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

            result = spiget_api.download_plugin_if_update(filename)

            if result.get("status"):
                Utils.status(result.get("message"))
            else:
                Utils.warning(result.get("message"))

    else:
        Utils.error(f"Action {args.action} does not exist")
