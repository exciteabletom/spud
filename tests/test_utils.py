from spud.utils import Utils
import unittest


class MyTestCase(unittest.TestCase):
    def test_split_title_case(self):
        title_case_words = "TestingThisMethod"

        self.assertEqual(
            Utils.split_title_case(title_case_words), "Testing This Method"
        )


if __name__ == "__main__":
    unittest.main()
