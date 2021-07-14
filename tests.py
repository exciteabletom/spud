import unittest
import api


class test_API(unittest.TestCase):
    spiget = api.SpigetAPI()

    def test_get_plugin_id(self):
        res = self.spiget.get_plugin_id("EssentialsX")
        self.assertTrue(type(res) == int)


if __name__ == "__main__":
    unittest.main()
