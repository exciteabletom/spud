import itertools
import operator
from typing import Union

import requests

from . import settings
from .type import Plugin, StatusDict, Author, Metadata
from .utils import Utils


class SpigetAPI:
    def __init__(
        self,
        base_api_url=settings.BASE_API_URL,
        user_agent=settings.USER_AGENT,
    ):
        self.base_api_url = base_api_url

        self.headers: dict = {
            "user-agent": user_agent,
        }

    def build_api_url(self, api_request: str) -> str:
        return f"{self.base_api_url}{api_request}"

    # noinspection PyDefaultArgument
    def call_api(self, api_request: str, params: dict = {}) -> requests.Response:
        return requests.get(
            self.build_api_url(api_request),
            params=params,
            headers=self.headers,
        )

    def get_plugin_by_id(self, plugin_id: int) -> Plugin:
        response = self.call_api(f"/resources/{plugin_id}")
        return response.json()

    def search_plugins(self, search_name: str) -> Union[list, None]:
        names = [search_name]
        split_name: str = Utils.split_title_case(search_name)
        if split_name:
            names.append(split_name)

        plugin_list: list[Plugin] = []

        for name in names:
            response = self.call_api(
                f"/search/resources/{name}",
                {
                    "field": "name",
                    "sort": "-downloads",
                    "size": 5,
                    "fields": "file,name,tag,version,downloads,id,author",
                },
            )
            if response.status_code == 200:
                plugin: Plugin = response.json()[0]
                plugin_list.append(plugin)

        if len(plugin_list) == 0:
            return None

        # Sort the list by highest downloads, then IDs
        plugin_list.sort(key=operator.itemgetter("downloads", "id"), reverse=True)

        # Remove duplicate ids from list
        plugin_list = [id_field[0] for id_field in itertools.groupby(plugin_list)]

        sorted_list: list[Plugin] = []
        for index, plugin in enumerate(plugin_list):
            # Exact match goes to first index
            if search_name.upper() == plugin["name"].upper():
                sorted_list.insert(0, plugin)

            # Fuzzy match goes to second index
            elif search_name.upper() in plugin["name"].upper():
                sorted_list.insert(1, plugin)

            # Everything else just gets appended to the end
            else:
                sorted_list.append(plugin)

        truncated_list: list[Plugin] = sorted_list[:10]

        for plugin in truncated_list:
            Utils.sanitise_api_plugin(plugin)
            # Author's name ==
            plugin["author"]["name"] = self.get_author(
                # Author's ID
                plugin["author"]["id"]
            )["name"]

        return truncated_list

    def download_plugin(self, plugin: Plugin, filename: str = "") -> StatusDict:
        """
        Download a plugin

        :param plugin: Dict containing plugin name, tag, and ID
        :param filename: Force a specific filename for the plugin instead of automatically making one
        :return: StatusDict
        """
        response = self.call_api(
            f"/resources/{plugin.get('id')}/download",
        )

        if not filename:
            plugin_jar_name = Utils.create_jar_name(plugin["name"])
        else:
            plugin_jar_name = filename

        with open(plugin_jar_name, "wb") as f:
            f.write(response.content)
            pass

        Utils.inject_metadata_file(plugin, plugin_jar_name)

        return {"status": True, "message": ""}

    def download_plugin_if_update(self, filename: str) -> StatusDict:
        """

        :param filename: Filename of a plugin
        :return: StatusDict
        """
        metadata: Union[Metadata, None] = Utils.load_metadata_file(filename)
        if not metadata:
            return {
                "status": False,
                "message": f"Couldn't load metadata for {filename}. Try reinstalling with spud first",
            }

        plugin_id: int = metadata["plugin_id"]
        plugin = self.get_plugin_by_id(plugin_id)

        local_version: int = metadata["plugin_version_id"]
        latest_version: int = plugin["version"]["id"]

        if local_version >= latest_version:
            return {"status": False, "message": ""}
        else:
            self.download_plugin(plugin, filename)
            return {
                "status": True,
                "message": f"Updated {plugin.get('name')} to latest version",
            }

    def get_author(self, author_id: int) -> Author:
        """
        Gets an Author dict from an ID

        :param author_id: The ID of an author
        :return: A dict representing the author
        """
        return self.call_api(f"/authors/{author_id}").json()
