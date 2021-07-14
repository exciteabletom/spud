import setuptools

from spugin import settings

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="spugin",
    version=settings.VERSION,
    author="Tommy Dougiamas",
    author_email="tom@digitalnook.net",
    description="A Minecraft Spigot plugin manager that adheres the Unix philosophy and Python best practices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/exciteabletom/spugin",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    package_dir={"spugin": "spugin"},
    packages=["spugin"],
    python_requires=">=3.6",
)
