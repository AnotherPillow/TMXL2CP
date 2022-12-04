import src.conv as conv
import src.tiled as tiled
import json
import os

ex = False

if not os.path.exists("TMXL\\content.json"):
    os.mkdir("TMXL/")
    ex = True
    

try:
    import json5
    import PIL
    import bs4
    import shutil
except ImportError as e:
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

