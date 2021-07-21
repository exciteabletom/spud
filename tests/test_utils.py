import unittest
from spud.utils import Utils, StatusDict


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

    def test_StatusDict(self):
        message = "Error Occurred!"
        status_dict = StatusDict(False, message)

        self.assertEqual(type(status_dict), StatusDict)
        self.assertEqual(status_dict.get("message"), message)
        self.assertFalse(status_dict.get("status"))

        status_dict = StatusDict(True)

        self.assertEqual(type(status_dict), StatusDict)
        self.assertEqual(status_dict.get("message"), "")
        self.assertTrue(status_dict.get("status"))


if __name__ == "__main__":
    unittest.main()
