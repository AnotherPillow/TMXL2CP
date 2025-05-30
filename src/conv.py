import os
import bs4
import shutil
import json
from PIL import Image

from src.utils import *

import src.tiled as tiled

contentPatcher = getBlankCP()
newCPManifest = {}
tmxlContent = getTMXL()
customLocations = []
customMapNames = []

TMXLAUTHOR = TMXLManifest()["Author"]

def main():
    if 'festivalSpots' in tmxlContent:
        for spot in tmxlContent['festivalSpots']:
            mapName = spot['map']
            date = mapNameToDate(mapName)
            x, y = spot['position']
            who = spot['name']

            positionChange = {
                "Action": "EditData",
                "Target": f"Data/Festivals/{date}",
                "TextOperations": [
                    {
                        "Operation": "Append",
                        "Target": [
                            "Entries",
                            "Set-Up_additionalCharacters"
                        ],
                        "Value": f"{who} {x} {y} {spot['direction']}",
                        "Delimiter": "/"
                    }
                ]
            }

            contentPatcher["Changes"].append(positionChange)
    
    if 'shops' in tmxlContent:
        for shop in tmxlContent['shops']:
            portraitPath = None

            if 'portraits' in shop:
                portraitFileName = f'assets/{shop["portraits"][0].split("/")[-1]}'
                portraitPath = f"Portraits/{shop['id']}"

                portraitChange = {
                    "Action": "Load",
                    "FromFile": portraitFileName,
                    "Target": portraitPath,
                }

                contentPatcher["Changes"].append(portraitChange)
            
            change = {
                "Action": "EditData",
                "Target": "Data/Shops",
                "Entries": {
                    shop['id']: {
                        "Items": [
                            {
                                "Price": i['price'] if 'price' in i else i['Price'], # Thanks SVE so much for using different cases
                                "TradeItemId": inventoryTypeToQualified(i['type']) + str(i['index']) 
                                    if 'index' in i 
                                    else (print(f"{i['name']} ({i['type']}) will fail due to being a custom item.") or 'This item will fail to load.'),
                                "AvailableStock": -1 if 'stock' not in shop else shop['stock']
                            } for i in shop['inventory']
                        ],
                        "Owners": [
                            {
                                "Name": shop['id'],
                                "Id": shop['id'],
                                "Portrait": portraitPath,
                            }
                        ]
                    }

                }
            }

            contentPatcher["Changes"].append(change)

    if 'addMaps' in tmxlContent:
        for map in tmxlContent["addMaps"]:
            fileName = map["file"].split("/")[-1]
            mapName = map["name"]
            customMapNames.append(mapName)

            mapchange = {
                "Action": "Load",
                "Target": f"Maps/Custom_{mapName}",
                "FromFile": f"assets/{fileName.replace('.tbin', '.tmx')}"
            }
            
            change = {
                "Action": "EditData",
                "Target": "Data/Locations",
                "Entries": {
                    f"Custom_{mapName}": {
                        "DisplayName": f'Custom_{mapName}',
                        "DefaultArrivalTile": (0, 0),
                        "CreateOnLoad": {
                            "MapPath": f'Maps/Custom_{mapName}'
                        },
                        "FormerLocationNames": [ mapName ]
                    }
                }
            }
            
            contentPatcher["Changes"].append(mapchange)
            contentPatcher["Changes"].append(change)
            
            if "addWarps" in map:
                warps = {
                    "Action": "EditMap",
                    "Target": f'Maps/Custom_{map["name"]}',
                }
                #split warps into a list with elements that are 5 items long
                warpList = [map["addWarps"][i:i+5] for i in range(0, len(map["addWarps"]), 5)][0]
                warpList2 = []
                for warp in warpList:
                    if warp.split(" ")[2] in customMapNames:
                        warp = warp.replace(warp.split(" ")[2], f'Custom_{warp.split(" ")[2]}')
                    warpList2.append(warp)
                warps["addWarps"] = warpList2

                for w in warps:
                    contentPatcher["Changes"].append(w)

    if 'onlyWarps' in tmxlContent:
        for warp in tmxlContent["onlyWarps"]:
            warps = {
                "Action": "EditMap",
                "Target": f'Maps/Custom_{warp["name"]}' if warp["name"] in customMapNames else f'Maps/{warp["name"]}',
            }
                #split warps into a list with elements that are 5 items long
            warpList = [warp["addWarps"][i:i+5] for i in range(0, len(warp["addWarps"]), 5)][0]
            warpList2 = []
            for warp in warpList:
                if warp.split(" ")[2] in customMapNames:
                    
                    warp = warp.replace(warp.split(" ")[2], f'Custom_{warp.split(" ")[2]}')
                warpList2.append(warp)
            warps["addWarps"] = warpList2
            contentPatcher["Changes"].append(warps)

            print('Custom warp added to map ' + map["name"])

    if 'spouseRooms' in tmxlContent:
        for spouseRoom in tmxlContent["spouseRooms"]:
            
            fileName = spouseRoom["file"].split("/")[-1].replace(".tbin", ".tmx")
            mn = f"{TMXLAUTHOR}_{spouseRoom['name']}_ROOM"
            editdata = {
                "Action": "EditData",
                "Target": "Data/Characters",
                "TargetField": [ "Entries", spouseRoom['name'] ],
                "Fields": {
                    "SpouseRoom": {
                        "MapAsset": mn,
                        "MapSourceRect": {
                            "X": 0,
                            "Y": 0,
                            "Width": 6,
                            "Height": 9,
                        }
                    },
                }
            }
            load = {
                "Action": "Load",
                "Target": f"Maps/{mn}",
                "FromFile": f"assets/{fileName}",
            }
            contentPatcher["Changes"].append(editdata)
            contentPatcher["Changes"].append(load)




    newCPManifest = TMXLManifest()
    newCPManifest["ContentPackFor"]["UniqueID"] = "Pathoschild.ContentPatcher"
    newCPManifest["UniqueID"] += ".TMXL2CP"
    if 'Dependencies' in newCPManifest:
        newCPManifest["Dependencies"] = [x for x in newCPManifest["Dependencies"] if x["UniqueID"] not in ['Platonymous.Toolkit', 'Platonymous.TMXLoader']]

    with open(f"CP{os.path.sep}manifest.json", "w") as f:
        json.dump(newCPManifest, f, indent=4)
        f.close()
    

    if not os.path.exists(os.path.join(os.getcwd(), "CP", "assets")):
        os.makedirs("CP{os.path.sep}assets{os.path.sep}")

    PIL_blankimages = []
    

    for root, dirs, files in os.walk(os.path.join(os.getcwd(), "TMXL", "assets")):
        for file in files:
            if file.endswith(".tbin"):
                print(f'Converting {file} to TMX... ', end='')
                tbinPath = os.path.join(root, file)
                    
                    
                tmxPath = os.path.join(root, file.replace(".tbin", ".tmx"))
                
                tiled.tbinConv(tbinPath, tmxPath)
                print(f'Done')
                print(f'Moving {file} to CP')
                shutil.copy(tmxPath, os.path.join(os.getcwd(), "CP", "assets"))
            elif file.endswith(".png") or file.endswith(".tsx"):
                print(f'Moving {file} to CP')
                shutil.copy(os.path.join(root, file), os.path.join(os.getcwd(), "CP", "assets"))
            else:
                tmxPath = os.path.join(root, file)
                
                print(f'Moving {file} to CP')
                shutil.copy(tmxPath, os.path.join(os.getcwd(), "CP", "assets"))
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), "CP", "assets")):
        for file in files:
            if file.endswith(".tmx"):
                tmxPath = os.path.join(root, file)
                #open tmxFile with utf-8 encoding
                with open(tmxPath, "r", encoding="utf-8") as tmxFile:
                    soup = bs4.BeautifulSoup(tmxFile.read(), "html.parser")
                    tmxFile.close()
                    #get the properties tag
                    #find all property tags in the properties tag
                propertyWarpTags = soup.find_all("property", {"name": "Warp"})
                for warp in propertyWarpTags:
                    if warp["value"] != "":
                        #   print(warp["value"])
                            #print(warp["value"])
                            #mapName = warp["value"].split(" ")[0]
                        warpsSplit = warp["value"].split(" ")
                        warps = []
                        for i in range(0, len(warpsSplit), 5):
                            chunk = warpsSplit[i:i+5]
                            warps.append(chunk)
                            #   print(warps)
                            
                        for i,w in enumerate(warps):
                                #   print(w)
                            if w[2] in customMapNames:
                                    #   print("yes")
                                w[2] = f'Custom_{w[2]}'
                                warps[i] = " ".join(w)
                            else:
                                warps[i] = " ".join(w)
                            #replace the warp property with the new value
                        warp["value"] = warps

                propertyActionTags = soup.find_all("property", {"name": "Action"})
                for action in propertyActionTags:
                    if action["value"].startswith("Warp ") or action["value"].startswith("LockedDoorWarp"):
                        print("Warp found")
                        mapName = action["value"].split(" ")[3]
                        if mapName in customMapNames:
                            action["value"] = action["value"].replace(mapName, f'Custom_{mapName}')
                    elif action["value"].startswith("Warp"):
                        print(f"{action['value']} found")
                    else:
                        pass
                    
                    
                #get all image tags with a source, with and height attribute
                images = soup.find_all("image", {"source": True, "width": True, "height": True})
                for image in images:
                    if not os.path.exists(os.path.join(os.getcwd(), "CP", "assets", image["source"])):
                        img = Image.new("RGBA", (int(image["width"]), int(image["height"])))

                        
                        try:
                            img.save(os.path.join(os.getcwd(), "CP", "assets", image["source"] + '.png'))
                        except:
                            image["source"] = image["source"].replace("/", "\\")
                            os.makedirs(os.path.join(os.getcwd(), "CP", "assets", image["source"]))
                            img.save(os.path.join(os.getcwd(), "CP", "assets", image["source"]+ ".png"))
                            
                        PIL_blankimages.append(image["source"])
                    
                
                
                with open(tmxPath, "w", encoding="utf-8") as tmxFile:
                        #   print(tmxPath)
                    tmxFile.write(str(soup))
                    tmxFile.close()
                    
                print(f"root: {root}")
                print(f"Path: {file}")
                print('')
                    
                fileFolderPath = root.replace(os.getcwd(), "")
                    
                if fileFolderPath.startswith("\\") or fileFolderPath.startswith("/"):
                    fileFolderPath = fileFolderPath[1:]

                assetPath = os.path.join(fileFolderPath, file)
                    
                if tiled.csvConv(assetPath):
                    print(f"Successfully converted {file} to CSV Formatting... ")
                else:
                    print(f"Failed to convert {file} to CSV Formatting...")
                
        #write the new contentPatcher file

    #delete the blank images
    for image in PIL_blankimages:
        try:
            os.remove(os.path.join(os.getcwd(), "CP", "assets", image + '.png'))
        except:
            pass

    if 'mergeMaps' in tmxlContent:
        for map in tmxlContent["mergeMaps"]:
            lastElement = map["file"].split("/")[-1]
            mapPath = f'CP/assets/{lastElement.replace(".tbin", ".tmx")}'
            wh = tiled.getMapWidthHeight(mapPath)
            
            if 'condition' in map:
                print(f'[WARN] CONDITION IGNORED FOR {map["name"]} PATCH FROM {map["file"]}')
            
            editMap = {
                "Action": "EditMap",
                "Target" : f'Maps/{map["name"]}',
                "FromArea": {
                    "X": map["sourceArea"][0] if 'sourceArea' in map else 0,
                    "Y": map["sourceArea"][1] if 'sourceArea' in map else 0,
                },
                "ToArea": {
                    "X": map["position"][0] if 'position' in map else 0,
                    "Y": map["position"][1] if 'position' in map else 0,
                    "Width": int(wh[0]),
                    "Height": int(wh[1])
                },
            }

            if 'sourceArea' in map:
                editMap["FromArea"]["Width"] = map["sourceArea"][2]
                editMap["FromArea"]["Height"] = map["sourceArea"][3]
            else:
                

                editMap["FromArea"]["Width"] = int(wh[0])
                editMap["FromArea"]["Height"] = int(wh[1])
                

            try:
                if map["removeEmpty"] == True:
                    editMap["PatchMode"] = 'Replace'
                elif map["removeEmpty"] == False:
                    editMap["PatchMode"] = 'Overlay'
            except:
                editMap["PatchMode"] = 'Overlay'

            fname = map["file"].split("/")[-1]
            editMap["FromFile"] = f'assets/{fname.replace(".tbin", ".tmx")}'
            
            contentPatcher["Changes"].append(editMap)

            try:
                if "addWarps" in map:
                    warps = {
                        "Action": "EditMap",
                        "Target": f'Maps/Custom_{map["name"]}' if map["name"] in customMapNames else f'Maps/{map["name"]}',
                    }
                    #split warps into a list with elements that are 5 items long
                    warpList = [map["addWarps"][i:i+5] for i in range(0, len(map["addWarps"]), 5)][0]
                    warpList2 = []

                    for warp in warpList:
                        if warp.split(" ")[2] in customMapNames:
                            warp = warp.replace(warp.split(" ")[2], f'Custom_{warp.split(" ")[2]}')
                        warpList2.append(warp)
                    warps["addWarps"] = warpList2
                    contentPatcher["Changes"].append(warps)
                    print('Custom warp added to map ' + map["name"])
            except KeyError:
                print("No warps to add")
                pass

        
    


    with open (os.path.join(os.getcwd(), f"CP{os.path.sep}content.json"), "w") as contentPatcherFile:
        contentPatcherFile.write(json.dumps(contentPatcher, indent=4))
        contentPatcherFile.close()
    print("")
    print("Conversion Complete")
    print("Remember to make any changes to now refer to the new map names in any other files you may have.")
    input("Press Enter to exit")