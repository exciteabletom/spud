# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
import unittest

from spud import cli


class TestCli(unittest.TestCase):
    def setUp(self) -> None:
        self.cli = cli.CLI()

    # TODO
