"""
Custom types used in the program.

TypedDicts:
    StatusDict
    Author
    PluginVersion
    Plugin
    Metadata
    Update
"""
from typing import TypedDict


class StatusDict(TypedDict):
    """Allows you to return a status value and an error/success message from a function"""

    status: bool
    message: str


class Author(TypedDict, total=False):
    """Represents a resource Author"""

    id: int
    name: str


class PluginVersion(TypedDict):
    """Represents a specific plugin version"""

    id: int
    uuid: str


class Plugin(TypedDict):
    """Represents a plugin"""

    file: dict
    name: str
    tag: str
    version: PluginVersion
    id: int
    str: int
    author: Author


class Metadata(TypedDict):
    """Represents the metadata values saved into jar files"""

    search_name: str
    plugin_id: int
    plugin_version_id: int


class Update(TypedDict):
    """Represents a specific update of a plugin received"""

    id: int
    title: str
    description: str
    date: int
    likes: int
