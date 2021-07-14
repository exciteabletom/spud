import argparse
import os

from pathlib import Path
from . import api
from .utils import Utils


def parse_args():
    parser = argparse.ArgumentParser(
        description="Spud: The plugin manager for your Spigot Minecraft server"
    )
    parser.add_argument("action", help="install, update, or remove", type=str)
    parser.add_argument("plugin_name", help="the name of the plugin", type=str)
    parser.add_argument(
        "-d",
        "--directory",
        dest="directory",
        help="path to plugins directory, defaults to `.`",
        type=str,
        default=".",
    )
    args = parser.parse_args()
    return args


def get_plugin_choice(plugin_list: list) -> dict:
    Utils.status("--------------------")
    for index, plugin in enumerate(plugin_list):
        Utils.status(f"{index} | {plugin.get('name')} | {plugin.get('tag')}")

    Utils.status("--------------------")

    chosen_ID: int = 0
    while True:
        try:
            chosen_ID = int(Utils.prompt("Select a plugin ID"))
        except ValueError:
            continue

        if 0 <= chosen_ID < len(plugin_list):
            return plugin_list[chosen_ID]
        else:
            continue


def main():
    args = parse_args()
    args.plugin_name = Utils.sanitise_input(args.plugin_name)
    os.chdir(Path(args.directory))

    spiget_api = api.SpigetAPI()
    if args.action == "install":
        plugin_list = spiget_api.search_plugins(args.plugin_name)
        plugin = get_plugin_choice(plugin_list)

        Utils.status(f"Installing {plugin.get('name')}")

        result: dict = spiget_api.download_plugin(plugin)

        if result.get("status"):
            Utils.status(f"{args.plugin_name} was installed successfully")
        else:
            Utils.error(result.get("error_message"))

    elif args.action == "update":
        Utils.error("Not implemented!")

    elif args.action == "remove":
        Utils.error("Not implemented!")
    else:
        Utils.error("Not implemented!")
