# Spud
![spudman logo](https://raw.githubusercontent.com/exciteabletom/spud/master/logo/spudman_tiny.png)


[![GPLv3 License](https://www.gnu.org/graphics/gplv3-88x31.png)](https://www.gnu.org/licenses/gpl-3.0.en.html)
[![GitHub Release](https://img.shields.io/github/release/exciteabletom/spud.svg?style=flat)](https://github.com/exciteabletom/spud/releases) 
[![PyPI downloads](https://img.shields.io/pypi/dm/spud-mc.svg)](https://pypistats.org/packages/spud-mc)
[![Code style: Black](https://img.shields.io/badge/code%20style-Black-000000.svg)](https://github.com/psf/black)


A cross-platform, [Spigot](https://www.spigotmc.org/) plugin manager that adheres to the
[Unix philosophy](https://en.wikipedia.org/wiki/Unix_philosophy) and Python best practices.

Some focuses of the project are:

1. Easy and simple commands (updating all your plugins is as simple as `spud update`)

1. Unlike other options like [pluGET](https://github.com/Neocky/pluGET), it adheres to Unix conventions and doesn't force you to use a GUI, making it easy to use in scripts.

1. Insisting upon readability, static type hinting, test-driven development, and consistent styling in the codebase.

1. Descriptive output and actionable error messages


## Installation
Python 3.8 or later is required

Install with `python -m pip install spud-mc`

Run `spud -h` to see all the options.


## Example usages
- Install a plugin: `spud install PluginName`

- Install a plugin without prompting for input: `spud -n install PluginName`

- Update all plugins in the working directory: `spud update`

- Update all plugins in `~/server/plugins`: `spud -d ~/server/plugins update`
 
- Update plugin `myplugin.jar`: `spud update myplugin.jar`

## Known Issues
- Some resources have lots of filler in the title. e.g. `[1.8-1.17] · PluginName |
😃 😃 😃 | Epic Gaming Moments`.
Spud tries its best to extract the plugin name, but it will fail if there is copious amounts of garbage in the title


- Spud can't update plugins it has not installed. Make sure to install the plugin with Spud first, so it can save a metadata file to the jar.


- Spud can't install resources not listed on https://spigotmc.org


- Spud can't install premium resources

## Setting up a dev environment
`git clone git@github.com:exciteabletom/spud`

`cd spud`

`python3 -m venv .venv`

Bash: `. .venv/bin/activate`

Windows PowerShell: `.venv\bin\activate.ps1`

`python3 -m pip install -r requirements.txt -r requirements-dev.txt`

`pre-commit install`

## Acknowledgements
Logo created by [zach_can_draw](https://instagram.com/zach_can_draw/)

