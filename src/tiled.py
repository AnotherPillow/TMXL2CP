import os, json
from tmxpy import TMXpy as tmxpy
from pathlib import Path

config = json.loads(open("config.json").read())

#check if Tiled is installed on all platforms
def checkTiled():
    #do different things for different platforms
    if os.name == 'nt':
        #check if Tiled is installed
        if os.path.exists("C:\Program Files\Tiled\Tiled.exe"):
            return [True, "C:\Program Files\Tiled\Tiled.exe"]
        else:
            return False
    elif os.name == 'posix':
        #check if Tiled is installed
        if os.path.exists("/usr/bin/tiled"):
            return [True, "/usr/bin/tiled"]
        else:
            return False
    elif os.path.exists("/Applications/Tiled.app"):
            return [True, "/Applications/Tiled.app"]
    elif os.path.exists(config["tiledPath"]):
        return [True, config["tiledPath"]]
    else:
        return [False, None]
            

def tbinConv(tbinPath, tmxPath, tiledPath):
    oldWorkingDir = os.getcwd()
    
    os.chdir(os.path.dirname(tiledPath))
    
    os.system(f'tiled --export-map "{tbinPath}" "{tmxPath}"')
    
    os.chdir(oldWorkingDir)

def csvConv(tmxPath, tiledPath):
    cwd = os.getcwd()

    tmxPath = os.path.join(cwd, tmxPath)
    scriptPath = os.path.join(cwd, "scripts", "formatConv.js")

    os.chdir(os.path.dirname(tiledPath))

    #command = f'"{tiledPath}" --evaluate "{scriptPath}" "{tmxPath}"'
    command = f'tiled --evaluate "{scriptPath}" "{tmxPath}"'
    print(command)

    _ = os.system(command)

    os.chdir(cwd)

    os.remove(tmxPath)
    os.rename(tmxPath.replace('.tmx', '_conv.tmx'), tmxPath)
    return
def getMapWidthHeight(tmxPath):
    tmx = tmxpy(
        [], 
        path=Path.joinpath(tmxPath)
    )
    
    return tmx.tmxDimensions