/// <reference types="@mapeditor/tiled-api" />

/**
 * Test Command:
 * "C:\Program Files\Tiled\Tiled.exe" --evaluate formatConv.js ../CP/assets/gv_diner_interior.tmx
 */

const args = tiled.scriptArguments;
const mapPath = args[0];

const newPath = mapPath.replace(/\.tmx$/, "_conv.tmx");

var map = tiled.mapFormat('tmx').read(mapPath);

if (map.layerDataFormat !== TileMap.CSV) map.layerDataFormat = TileMap.CSV;



//save the map
try {
    tiled.mapFormat('tmx').write(map, newPath);
    console.log("Map saved to " + newPath);
} catch (e) {
    console.log("Error saving map: " + e);
}