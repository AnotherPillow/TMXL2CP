/// <reference types="@mapeditor/tiled-api" />

/**
 * Test Command:
 * "C:\Program Files\Tiled\Tiled.exe" --evaluate spouseRoomResize.js ../CP/assets/gv_diner_interior.tmx
 */

const args = tiled.scriptArguments;
const mapPath = args[0];

const newPath = mapPath.replace(/\.tmx$/, "_conv.tmx");

var map = tiled.mapFormat('tmx').read(mapPath);

map.resize(Qt.size(6, 9), null, true);


try {
    tiled.mapFormat('tmx').write(map, newPath);
    console.log("Map saved to " + newPath);
} catch (e) {
    console.log("Error saving map: " + e);
}