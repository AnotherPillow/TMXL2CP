# TMXL2CP

## _AS OF 24/02/24, 1.6 IS REQUIRED TO RUN, 1.5.6 IS NO LONGER COMPATIBLE_

## About

This is a tool to convert TMXLoader/TMX Map toolkit mods to CP mods.

## Features

* Converts all tbin files to tmx files.
* Renames all map property warps to to fit with the CP requirement for a prefixed `Custom_` before the map name.
* Renames all `LockedDoorWarps` and `Warp` Action TileDatas to the prefixed `Custom_` before the map name.
* Converts all maps to CSV layer format.
* Has support for `mergeMaps`, `addMaps`, `onlyWarps` and `spouseRooms`.
* Changes CP `PatchMode` field to be based on the TMXL `removeEmpty` field, if applicable.
* Convert all `festivalSpots` to use `Data/festivals/[date]`.
* Convert all shops to `Data/Shops`.

## Usage

1. Download the [source code](https://github.com/AnotherPillow/TMXL2CP/archive/refs/heads/main.zip) and unzip it.
2. Install Python, ideally 3.11 or later.
3. Edit the config.json to point to your **game folder** (the one containing `Stardew Valley.exe`) (backslashes must be escaped).
4. Place your TMXL mod in `TMXL/`, so that the `content.json` is `TMXL/content.json`. If this folder doesn't exist, just make it relative to the `main.py`.
5. Run `main.py`, this is likely via `py main.py`, but could also be `python main.py` or `python3 main.py`.
6. Find your converted mod in `CP/`.
7. Make sure to do any manual edits in other portions of the mod, such as NPC schedules, disposition data, etc.

If there is an error automatically installing dependencies, you can install them manually via `pip install -r requirements.txt`. You may need to use `py -m pip`, `python -m pip` or `python3 -m pip` instead of `pip` depending on your Python installation.

## Improvements/Contributions

If you have any improvements or contributions, please feel free to make a pull request or open an issue.
