from pathlib import Path

import requests

import settings
from .utils import Utils


class SpigetAPI:
    headers: dict = {
        "user-agent": settings.USER_AGENT,
    }

    @staticmethod
    def build_api_url(api_request: str) -> str:
        return f"{settings.API_URL}{api_request}"

    # noinspection PyDefaultArgument
    def call_api(self, api_request: str, params: dict = {}) -> requests.Response:
        response: requests.Response = requests.get(
            self.build_api_url(api_request),
            params=params,
        )
        return response

    def get_plugin_id(self, plugin_name: str) -> int:
        response = self.call_api(
            f"/search/resources/{plugin_name}",
            {
                "field": "name",
                "sort": "-downloads",
                "fields": "id,",
            },
        )

        plugin_id: int = response.json()[0].get("id")
        return plugin_id

    def download_plugin(self, plugin_name: str) -> bool:
        plugin_id = self.get_plugin_id(plugin_name)
        response = self.call_api(
            f"/resources/{plugin_id}/download",
        )

        safe_plugin_name = Utils.create_jar_name(plugin_name)
        with open(
            Path(f"{settings.PLUGIN_FOLDER}/{safe_plugin_name}.jar").__str__(), "wb"
        ) as f:
            f.write(response.content)
            pass

        return True
