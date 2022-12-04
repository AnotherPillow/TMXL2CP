import os
import json
import json5

def getBlankCP():
    cpPath = os.path.join(os.getcwd(), "src\\blank\\content.json")
    blankContentPatcher = json.loads(open(cpPath).read())
    #print(blankContentPatcher)
    return blankContentPatcher
def getTMXL():
    tmxlPath = os.path.join(os.getcwd(), "TMXL\\content.json")
    #open the file with utf-8 encoding
    with open(tmxlPath, encoding='utf-8') as f:
        #read the file as a string
        tmxlContent = f.read()
        #parse the string as json
        tmxlContent = json5.loads(tmxlContent)
        f.close()
    return tmxlContent
def blankManifest():
    manifestPath = os.path.join(os.getcwd(), "src\\blank\\manifest.json")
    with open(manifestPath, encoding='utf-8') as f:
        manifest = f.read()
        manifest = json5.loads(manifest)
        f.close()
    return manifest
def TMXLManifest():
    manifestPath = os.path.join(os.getcwd(), "TMXL\\manifest.json")
    with open(manifestPath, encoding='utf-8') as f:
        manifest = f.read()
        manifest = json5.loads(manifest)
        f.close()
    return manifest