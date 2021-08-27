import os
import unittest
from pathlib import Path

from spud import api


class TestAPI(unittest.TestCase):
    spiget = api.SpigetAPI()

    def tearDown(self):
        # Cleanup jar files saved during testing
        for file in os.listdir():
            if file.endswith(".jar"):
                os.remove(file)

    def test_build_api_url(self):
        api_path = "/testing/api/test"
        self.assertEqual(
            self.spiget.build_api_url("/testing/api/test"),
            f"{self.spiget.base_api_url}{api_path}",
        )

    def test_search_plugins(self):
        res = self.spiget.search_plugins("LuckPerms")
        # returns list
        self.assertTrue(type(res) == list)
        # of dicts
        self.assertTrue(type(res[0]) == dict)
        # that are not empty
        self.assertTrue(type(res[0]))

    def test_download_plugin(self):
        plugin = self.spiget.search_plugins("LuckPerms")[0]
        result = self.spiget.download_plugin(plugin)
        self.assertTrue(result.get("status"))
        self.assertTrue("LuckPerms.jar" in os.listdir())
        self.assertTrue(Path("LuckPerms.jar").stat().st_size > 100000)


if __name__ == "__main__":
    unittest.main()
