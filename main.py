# import src.conv as conv
import src.tiled as tiled
from src.functions import downloadToasterMapCLI
import json
import os
import shutil

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

if not os.path.exists("bin/"):
    os.mkdir("bin/")
    

try:
    import json5, PIL, bs4, shutil
except (ImportError, ModuleNotFoundError):
    print("Installing dependencies...")
    if os.name == "nt":
        os.system("py -m pip install -r requirements.txt")
    else:
        os.system("python3 -m pip install -r requirements.txt")

    import json5, PIL, bs4, shutil

import src.conv as conv

if ex:
    print("Created TMXL folder. Please place your TMXL mod in the TMXL folder and press enter to continue.")
    input()

config = json.loads(open("config.json").read())
if not config["ran_before"]:
    downloadToasterMapCLI()
    config["ran_before"] = True
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
        f.close()

if not os.path.exists('bin/xTile.dll'):
    shutil.copyfile(os.path.join(config['game_folder'], 'xTile.dll'), 'bin/xTile.dll')


conv.main()

