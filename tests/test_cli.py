# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
import unittest
from pathlib import Path

from spud import cli


class TestCli(unittest.TestCase):
    def test_parse_args(self):
        args = cli.CLI.parse_args(
            ["spud", "-n", "-d", "/home/test", "install", "LuckPerms", "EssentialsX"]
        )
        self.assertTrue(args.noninteractive)
        self.assertEqual(args.plugins, ["LuckPerms", "EssentialsX"])
        self.assertEqual(args.action, "install")
        self.assertEqual(args.directory, Path("/home/test"))

        args = cli.CLI.parse_args(["spud", "update", "LuckPerms", "EssentialsX"])
        self.assertFalse(args.noninteractive)
        self.assertEqual(args.plugins, ["LuckPerms", "EssentialsX"])
        self.assertEqual(args.action, "update")
        self.assertEqual(Path(args.directory).absolute(), Path.cwd().absolute())
