import os
import unittest

from spud import api


class TestAPI(unittest.TestCase):
    spiget = api.SpigetAPI()

    def tearDown(self):
        # Cleanup jar files saved during testing
        for file in os.listdir():
            if file.endswith(".jar"):
                os.remove(file)

    def test_search_plugins(self):
        res = self.spiget.search_plugins("EssentialsX")
        self.assertTrue(type(res) == list and type(res[0]) == dict)

    def test_download_plugin(self):
        plugin = self.spiget.search_plugins("EssentialsX")[0]
        result = self.spiget.download_plugin(plugin)
        self.assertTrue(result.get("status"))


if __name__ == "__main__":
    unittest.main()
