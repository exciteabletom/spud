"""
Entrypoint for running an instance of the cli. Used by setuptools when installing an entrypoint.

Functions:
    init - Initialise the CLI
"""
from .cli import CLI


def init():
    """Initalise the CLI"""
    CLI()
