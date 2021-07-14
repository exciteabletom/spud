import argparse
import os

from pathlib import Path
from . import api
from .utils import Utils


def parse_args():
    parser = argparse.ArgumentParser(description="Manage Spigot server plugins")
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


def main():
    args = parse_args()
    args.plugin_name = Utils.sanitise_input(args.plugin_name)
    os.chdir(Path(args.directory))

    spiget_api = api.SpigetAPI()
    if args.action == "install":
        Utils.status(f"Installing {args.plugin_name}")
        result: dict = spiget_api.download_plugin(args.plugin_name)

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
