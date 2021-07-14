import requests

import settings


class SpigetAPI:
    headers: dict = {
        "user-agent": settings.USER_AGENT,
    }

    @staticmethod
    def build_api_url(api_request: str) -> str:
        return f"{settings.API_URL}{api_request}"

    def call_api(self, api_request: str, params: dict) -> dict:
        response: requests.Response = requests.get(
            self.build_api_url(api_request),
            params=params,
        )

        list_response: list = response.json()
        return list_response

    def get_plugin_id(self, plugin_name: str) -> int:
        result: dict = self.call_api(
            f"/search/resources/{plugin_name}",
            {
                "field": "name",
                "sort": "-downloads",
                "fields": "versions",
            },
        )

        plugin_id: int = result[0].get("versions")[0].get("id")
        return plugin_id

    # def download_plugin(self, plugin_id):
