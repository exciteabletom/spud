import setuptools

from spud import settings

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="spud-mc",
    version=settings.VERSION,
    author="Tommy Dougiamas",
    author_email="tom@digitalnook.net",
    description="A Minecraft Spigot plugin manager that adheres to the Unix philosophy and Python best practices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/exciteabletom/spud",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    entry_points={
        "console_scripts": ["spud = spud.__main__:init"],
    },
    package_dir={"spud": "spud"},
    packages=["spud"],
    python_requires=">=3.6",
)
