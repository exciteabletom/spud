"""
setup.py file for installing Spud with pip
"""
import setuptools

from spud import settings

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

requirements = []
with open("requirements.txt", "r", encoding="utf-8") as f:
    for line in f:
        requirements.append(line.strip())

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
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: System :: Software Distribution",
        "Typing :: Typed",
    ],
    entry_points={
        "console_scripts": ["spud = spud.__main__:init"],
    },
    package_dir={"spud": "spud"},
    packages=["spud"],
    install_requires=requirements,
    python_requires=">=3.8",
)
