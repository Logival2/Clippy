# Clippy
WIP, launch main.py with the map name as argument, otherwise a map will be generated (still experimental)

Turn by Turn for performance, allows a more thoughtful gameplay as permadeath is enabled  

## Multiplayer coop (4) ?  
ECS server only, will send all the screen to each player everytime?
12000 (unicode) chars

## Procedural generation  
For regions: [Voronoi diagram](https://en.wikipedia.org/wiki/Voronoi_diagram)
```The process involves procedurally generated basic elements like elevation, rainfall, mineral distribution, drainage and temperature.[1] For example, a high-rainfall and low-drainage area would make a swamp. Areas are thus categorized into biomes, which have two variables: savagery and alignment.[10] They have their own specific type of plant and animal populations. The next phase is erosion—which the drainage simulates. Rivers are created by tracing their paths from the mountains (which get eroded) to its end which is usually an ocean; some form into lakes.[11] The salinity field defines oceans, mangroves or alluvial plains. Names are generated for the biomes and rivers.[10] The names depend on the area's good/evil variable (the alignment) and though in English, they are originally in one of the four in-game languages of dwarves, elves, humans and goblins; these are the four main races in any generated world.[11]
After a few minutes the world is populated and its history develops for the amount of in-game years selected in the history parameter. Civilizations, races and religions spread and wars occur,[12] with the "population" and "deaths" counters increasing.[7] The ticker stops at the designated "years" value, at which point the world can be saved for use in any game mode. Should the player choose to retire a fortress, or should they be defeated, this world will persist and will become available for further games.```

## IA ecosystems  
[The Rise of the Systemic Game | Game Maker's Toolkit](https://www.youtube.com/watch?v=SnpAAX9CkIc)  
[Dwarf Fortress](https://en.wikipedia.org/wiki/Dwarf_Fortress)  


#### Strange animals made with Conway game of life (mushroom like?)  

#### Simulate water, and food  


## Colored CLI
Using curses (python wrapper around ncurses)  
https://jonasjacek.github.io/colors/ for color list  

#### Menus  
- Character creation  

#### Unicode chars display  
https://fr.wikipedia.org/wiki/Table_des_caract%C3%A8res_Unicode_(0000-0FFF)  
