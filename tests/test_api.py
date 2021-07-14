import unittest
from spugin import api


class TestAPI(unittest.TestCase):
    spiget = api.SpigetAPI()

    def test_get_plugin_id(self):
        res = self.spiget.get_plugin_id("EssentialsX")
        self.assertTrue(type(res) == int)

    def test_download_plugin(self):
        result = self.spiget.download_plugin("Better Giants")
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
