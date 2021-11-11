"""
Classes for interacting with APIs.

classes:
    SpigetAPI - Helps interacting with the Spiget API
"""
from __future__ import annotations

import base64
import itertools
import operator
from typing import Union

from bs4 import BeautifulSoup

import requests
from requests import HTTPError

from . import settings
from .type import Plugin, StatusDict, Author, Metadata, Update
from .utils import Utils


class SpigetAPI:
    """
    A class to represent a connection with the Spiget API
    """

    def __init__(
        self,
        base_api_url: str = settings.BASE_API_URL,
        user_agent: str = settings.USER_AGENT,
    ) -> None:
        """
        Initialise an instance of the Spiget API

        :param base_api_url: The root API http URL, default: settings.BASE_API_URL
        :param user_agent: The user-agent header to send with requests, default: settings.USER_AGENT
        """
        self.base_api_url = base_api_url

        self.headers: dict = {
            "user-agent": user_agent,
        }

    def build_api_url(self, endpoint: str) -> str:
        """Append an endpoint to the base API url and return it"""
        return f"{self.base_api_url}{endpoint}"

    def call_api(self, endpoint: str, params=None) -> requests.Response:
        """
        Call an API endpoint

        :param endpoint: The endpoint to call
        :param params: Request body as a dict (optional)
        :returns: A Response object
        """
        if params is None:
            params = {}

        response = requests.get(
            self.build_api_url(endpoint),
            params=params,
            headers=self.headers,
        )
        if str(response.status_code).startswith("5"):
            raise HTTPError

        return response

    def get_plugin_by_id(self, plugin_id: int) -> Plugin:
        """
        Get a Plugin using an ID.

        :returns: A dict of type Plugin
        """
        response = self.call_api(f"/resources/{plugin_id}")
        return response.json()

    def search_plugins(self, query: str) -> list[Plugin]:
        """
        Search for plugins using a query

        :returns: A list of Plugin dicts, sorted by relevance to the query
        """
        names = [query]
        split_name: str = Utils.split_title_case(query)
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
            return []

        # Sort the list by highest downloads, then IDs
        plugin_list.sort(key=operator.itemgetter("downloads", "id"), reverse=True)

        # Remove duplicate ids from list
        plugin_list = [id_field[0] for id_field in itertools.groupby(plugin_list)]

        sorted_list: list[Plugin] = []
        for plugin in plugin_list:
            # Exact match goes to first index
            if query.upper() == plugin["name"].upper():
                sorted_list.insert(0, plugin)

            # Fuzzy match goes to second index
            elif query.upper() in plugin["name"].upper():
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

        :param plugin: Plugin dict
        :param filename: Force a filename for the plugin instead of inferring it
        :return: StatusDict
        """
        response = self.call_api(
            f"/resources/{plugin['id']}/download",
        )
        if response.status_code != 200:
            return {
                "status": False,
                "message": "Could not download resource due to an unknown error. "
                "This can sometimes happen with external resources.",
            }

        if not filename:
            plugin_jar_name = Utils.create_jar_name(plugin["name"])
        else:
            plugin_jar_name = filename

        with open(plugin_jar_name, "wb") as file:
            file.write(response.content)

        Utils.inject_metadata_file(plugin, plugin_jar_name)

        return {"status": True, "message": f"Downloaded {plugin_jar_name}"}

    def get_plugin_info_if_update(self, metadata: Metadata) -> Union[Plugin, None]:
        """
        Get a Plugin dict for a plugin if it has been updated.

        :param metadata: A Metadata dict
        :returns: A Plugin dict if there was an update, otherwise None
        """
        plugin_id: int = metadata["plugin_id"]
        plugin = self.get_plugin_by_id(plugin_id)

        local_version: int = metadata["plugin_version_id"]
        latest_version: int = plugin["version"]["id"]

        if local_version >= latest_version:
            return None

        return plugin

    def get_author(self, author_id: int) -> Author:
        """
        Gets an Author dict from an ID

        :param author_id: The ID of an author
        :return: A dict representing the author
        """
        return self.call_api(f"/authors/{author_id}").json()

    def get_latest_update_info(self, plugin: Plugin) -> Update:
        """
        Get information about the latest update of a plugin

        :param plugin: A Plugin dict
        :return: An Update dict
        """
        response = self.call_api(f"/resources/{plugin['id']}/updates/latest")
        response.raise_for_status()

        update: Update = response.json()
        # Decode base64
        update["description"] = bytes.decode((base64.b64decode(update["description"])))
        # Convert html to plaintext
        update["description"] = " ".join(
            BeautifulSoup(update["description"], "html.parser").stripped_strings
        )
        # Remove duplicate newlines and spaces
        update["description"] = update["description"].replace("  ", " ")
        update["description"] = update["description"].replace("\r\n", "\n")
        update["description"] = update["description"].replace("\n\n", "\n")

        if len(update["description"]) > 1500:
            update["description"] = update["description"][:1500] + "..."
        return update
