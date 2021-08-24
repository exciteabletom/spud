import unittest

from spud.types import StatusDict
from spud.utils import Utils


class MyTestCase(unittest.TestCase):
    def test_split_title_case(self):
        title_case_words = "TestingThisMethod"

        self.assertEqual(
            Utils.split_title_case(title_case_words), "Testing This Method"
        )

    def test_sanitise_api_plugin(self):
        name = "1.13-1.17 😃| Plugin Name 😃| 😃The Greatest plugin in the universe!!!!"
        final_name = "Plugin Name"

        tag = "1.17 supported | unit tests!"
        final_tag = "1.17 supported - unit tests!"

        result = Utils.sanitise_api_plugin(
            {
                "name": name,
                "tag": tag,
            }
        )

        self.assertEqual(result.get("name"), final_name)
        self.assertEqual(result.get("tag"), final_tag)


if __name__ == "__main__":
    unittest.main()
