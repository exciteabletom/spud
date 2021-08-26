from typing import TypedDict


class StatusDict(TypedDict):
    status: bool
    message: str


class Author(TypedDict, total=False):
    id: int
    name: str


class PluginVersion(TypedDict):
    id: int
    uuid: str


class Plugin(TypedDict):
    file: dict
    name: str
    tag: str
    version: PluginVersion
    id: int
    str: int
    author: Author


class Metadata(TypedDict):
    search_name: str
    plugin_id: int
    plugin_version_id: int


class Update(TypedDict):
    id: int
    title: str
    description: str
    date: int
    likes: int
