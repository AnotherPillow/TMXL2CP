/// <reference types="@mapeditor/tiled-api" />

/**
* Test Command:
* "C:\Program Files\Tiled\Tiled.exe" --evaluate getMapSize.js ../CP/assets/gv_diner_interior.tmx
*/

const args = tiled.scriptArguments;
const mapPath = args[0];

const debug = false;

const txtPath = mapPath.replace(/\.tmx$/, "_maxSize.txt");

if (debug) console.log(`
DEBUG INFO
mapPath: ${mapPath}
txtPath: ${txtPath}
args: ${args}
`)

var map = tiled.mapFormat('tmx').read(mapPath);

//console.log(`width=${map.width}; height=${map.height};`);

var file = new TextFile(txtPath, TextFile.WriteOnly);
file.write(`width=${map.width}; height=${map.height};`);
file.commit();