# Spud
[![GPLv3 License](https://www.gnu.org/graphics/gplv3-88x31.png)](https://www.gnu.org/licenses/gpl-3.0.en.html) [![GitHub Release](https://img.shields.io/github/release/exciteabletom/spud.svg?style=flat)]() [![PyPi Version](https://img.shields.io/pypi/v/spud-mc.svg)](https://pypi.python.org/pypi/spud-mc/)

A cross-platform, [Spigot](https://www.spigotmc.org/) plugin manager that adheres to
[Unix philosophy](https://en.wikipedia.org/wiki/Unix_philosophy) and conventions.

Work in progress.

## Installation
Install with `pip install spud-mc`

Run `spud -h` to see all the options.


## Example usages
- Install a plugin: `spud install PluginName`
- Install a plugin without prompting for input: `spud -n install PluginName`
- Update all plugins in the working directory: `spud update`
- Update all plugins in `~/server/plugins`: `spud -d ~/server/plugins update`
- Update plugin `myplugin.jar`: `spud update myplugin.jar` or `spud update myplugin`

## Known Issues
- Some resources have lots of filler in the title. e.g. `[1.8-1.17] · PluginName |
😃 😃 😃 | Epic Gaming Moments`.
Spud tries its best to extract the plugin name, but it will fail if there is copious amounts of garbage in the title


- Spud can't update plugins it has not installed. Make sure to install the plugin with Spud first, so it can save a metadata file to the jar.


- Spud can't install resources not listed on https://spigotmc.org

## Acknowledgements
Inspired by [pluGET](https://github.com/Neocky/pluGET)

