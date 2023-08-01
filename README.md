# Great beginning of a platform game

Initial idea --> move the player through the map and collect coins. Move with the arrows and avoid lava.

See screenshot below:
![g](https://github.com/Paularossi/Platform-game/assets/46716589/f363179b-7f04-436e-998f-77115196e530)

## Requirements
For the Python part you only need to have the _arcade_ library downloaded. Just run the main\main.py file to start the game.

For the maps, I am using a different app called Tiled, it's quite intuitive for creating maps, once you get the hang of it. Keep in mind that you'll need to find other tilesets online if you want to add new objects, backgrounds, etc. 

You can for example google "grass tileset", download it, load it into your Tiled map, and then add the tiles you need. Note that you might have to resize some of the tile images as they could be too big or too small for the map.

## Current status 
Right now everything works, but there is only one simple map that needs to be extended.
### Next steps 
- add a "door" that would take the player to the next levels (should be an entire different map)
- potentially add more (and better quality) images for the player choice
- add a welcome screen (start game, settings, etc.) and a game over screen (right now the game just restarts if you go in the lava)
- fix the screen size (there is some weird black empty space??)
