# TMXL2CP

## About

This is a tool to convert TMXLoader/TMX Map toolkit mods to CP mods.

## Features

* Converts all tbin files to tmx files.
* Renames all map property warps to to fit with the CP requirement for a prefixed `Custom_` before the map name.
* Renames all `LockedDoorWarps` and `Warp` Action TileDatas to the prefixed `Custom_` before the map name.
* Converts all maps to CSV layer format.
* Has support for `mergeMaps`, `addMaps`, `onlyWarps` and `spouseRooms`.
* Changes CP `PatchMode` field to be based on the TMXL `removeEmpty` field, if applicable.

## Usage

1. Download the latest release.
2. Install the latest version of [Python 3](https://www.python.org/downloads/).
3. Place your TMXL mod in `TMXL/`, so that the `content.json` is in `TMXL/content.json`.
4. Run `main.py`, this is likely via `py main.py`, but could also be `python main.py` or `python3 main.py`.
5. Find your converted mod in `CP/`.
6. Make sure to do any manual edits in other portions of the mod, such as NPC schedules, disposition data, etc.

## Improvements/Contributions

If you have any improvements or contributions, please feel free to make a pull request or open an issue.

## Known Issues

1. Does not work on Windows Subsystem for Linux (WSL) likely due to file paths.
