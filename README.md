# Spud
A cross-platform, [Spigot](https://www.spigotmc.org/) plugin manager that adheres to
[Unix philosophy](https://en.wikipedia.org/wiki/Unix_philosophy) and conventions.

Work in progress.

## Installation
Install with `pip install spud-mc`

Run `spud -h` to see all the options.

Inspired by [pluGET](https://github.com/Neocky/pluGET)

## Known Issues
- Some resources have lots of filler in the title. e.g. `[1.8-1.17] · PluginName |
😃 😃 😃 | Epic Gaming Moments`.
Spud tries it's best to extract the plugin name from titles like this but it will fail if there is copious amounts of
garbage in the title


- Spud can't update plugins it hasn't installed. Make sure to install the plugin with Spud first so it can save a
metadata file to the jar.
