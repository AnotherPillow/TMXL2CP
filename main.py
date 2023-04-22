import src.conv as conv
import src.tiled as tiled
import json
import os
import sys

ex = False

if not os.path.exists("TMXL\\content.json"):
    #check if TMXL/ exists
    if not os.path.exists("TMXL/"):
        os.mkdir("TMXL/")
        ex = True
    else:
        print("Please place your TMXL mod in the TMXL folder so that the content.json is in TMXL/content.json")
        input("Press enter to exit...")
        exit()

#check if the folder CP exists
if not os.path.exists("CP/"):
    os.mkdir("CP/")
    

try:
    import json5, PIL, bs4, shutil
except (ImportError, ModuleNotFoundError):
    print("Installing dependencies...")
    if os.name == "nt":
        os.system("py -m pip install -r requirements.txt")
    else:
        os.system("python3 -m pip install -r requirements.txt")

    import json5, PIL, bs4, shutil
    

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

