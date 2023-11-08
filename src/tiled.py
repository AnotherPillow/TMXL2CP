import os, json
from tmxpy import tmxpy, XMLtoCSV
from pathlib import Path
from .functions import ToasterMapCLIFileName

config = json.loads(open("config.json").read())

def tbinConv(tbinPath, tmxPath):#
    mapcliFolder = os.path.join(os.getcwd(), 'bin')
    oldCwd = os.getcwd()
    cmd = f'{ToasterMapCLIFileName.replace(".exe", "")} "{tbinPath}" "{tmxPath}"'
    
    os.chdir(mapcliFolder)
    os.system(cmd)
    os.chdir(oldCwd)

    # print('Ran...')

def csvConv(tmxPath):
    try:
        XMLtoCSV(tmxPath, tmxPath)
        return True
    except Exception as e:
        print(e)
        return False
def getMapWidthHeight(tmxPath):
    tmx = tmxpy(
        [], 
        path=Path(tmxPath)
    )
    
    return tmx.tmxDimensions