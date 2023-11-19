import os
import json
import json5
import requests

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

def mapNameToDate(mapName):
    return {
        'Town-EggFestival': 'spring13',
        'Forest-FlowerFestival': 'spring24',
        'Beach-Luau': 'summer11',
        'Beach-Jellies': 'summer28',
        'Town-Fair': 'fall16',
        'Town-Halloween': 'fall27',
        'Forest-IceFestival': 'winter8',
        'Town-Christmas': 'winter25',
    }[mapName]

def getToasterMapCLIDownloadLink(link=True):
    VERSION = '1.0.0'
    if os.name == 'nt':
        filename = 'ToasterMapCLI-win.exe'
        if link:
            return f'https://github.com/ToasterSDV/ToasterMapCLI/releases/download/v{VERSION}/ToasterMapCLI-win.exe'
        else:
            return filename
    elif os.name == 'posix':
        filename = 'ToasterMapCLI-osx'
        if link:
            return f'https://github.com/ToasterSDV/ToasterMapCLI/releases/download/v{VERSION}/ToasterMapCLI-osx'
        else:
            return filename
    else:
        filename = 'ToasterMapCLI'
        if link:
            return f'https://github.com/ToasterSDV/ToasterMapCLI/releases/download/v{VERSION}/ToasterMapCLI-linux'
        else:
            return filename
    
ToasterMapCLIFileName = getToasterMapCLIDownloadLink(False)
def downloadToasterMapCLI():
    link = getToasterMapCLIDownloadLink()

    print('Downloading ToasterMapCLI...')
    
    download = requests.get(link)
    open(f'./bin/{ToasterMapCLIFileName}', 'wb').write(download.content)

    print('Downloaded and saved ToasterMapCLI...')

def inventoryTypeToQualified(type):
    match type:
        case 'Object':
            return '(O)'
        case 'MeleeWeapon':
            return '(W)'
        case 'Wallpaper':
            return '(WP)'
        case 'Furniture':
            return '(F)'
        case _:
            return ''
    