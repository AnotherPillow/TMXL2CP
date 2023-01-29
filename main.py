import src.conv as conv
import src.tiled as tiled
import json
import os
import sys

##check if version is 3.11 or higher
if sys.version_info[0] < 3 and sys.version_info[1] < 11:
    print("Python version is too low. Please update to 3.11 or higher")
    input()
    exit()

ex = False

if not os.path.exists("TMXL\\content.json"):
    os.mkdir("TMXL/")
    ex = True

#check if the folder CP exists
if not os.path.exists("CP/"):
    os.mkdir("CP/")
    

try:
    import json5
    import PIL
    import bs4
    import shutil
except (ImportError, ModuleNotFoundError):
    print("Installing dependencies...")
    os.system("py -m pip install -r requirements.txt")

if ex:
    print("Created TMXL folder. Please place your TMXL mod in the TMXL folder and press enter to continue.")
    input()

config = json.loads(open("config.json").read())
if not config["ran_before"]:
    print("You may need to change the path to Tiled in config.json")
    print("You will also have to enable the tbin plugin in Tiled")
    print("If you don't have Tiled installed, you can download it from https://www.mapeditor.org/")
    config["ran_before"] = True
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
        f.close()


if not tiled.checkTiled():
    print("Tiled is not installed")
    print("----------------------")
    print("Please install Tiled and enable the tbin plugin")


conv.main()

