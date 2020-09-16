# Clippy
``./python3 main.py`` to launch a game using world generation, otherwise specify the map name as an argument  

## The game
Theme: A space explorator crashed on a planet, must find all the needed parts for his spaceship  

#### Mechanics
Turn by Turn?  
Permadeath?  

## Character creation ?

## Multiplayer coop (4 players)

## IA ecosystems  
[The Rise of the Systemic Game | Game Maker's Toolkit](https://www.youtube.com/watch?v=SnpAAX9CkIc)  
[Dwarf Fortress](https://en.wikipedia.org/wiki/Dwarf_Fortress)  
[Coding Adventure: Simulating an Ecosystem](https://www.youtube.com/watch?v=r_It_X7v-1E)  

#### Strange animals made with Conway game of life (mushroom like?)  

#### Simulate water, and food  

## Procedural World Generation  

#### Example from dwarf fortress
```
The process involves procedurally generated basic elements like rainfall, mineral distribution, drainage and temperature.
For example, a high-rainfall and low-drainage area would make a swamp. Areas are thus categorized into biomes, which have two variables: savagery and alignment.
They have their own specific type of plant and animal populations.
The next phase is erosion—which the drainage simulates. Rivers are created by tracing their paths from the mountains (which get eroded) to its end which is usually an ocean; some form into lakes.[11] The salinity field defines oceans, mangroves or alluvial plains.
Names are generated for the biomes and rivers. The names depend on the area's good/evil variable (the alignment) and though in English, they are originally in one of the four in-game languages of dwarves, elves, humans and goblins; these are the four main races in any generated world.[11]
After a few minutes the world is populated and its history develops for the amount of in-game years selected in the history parameter. Civilizations, races and religions spread and wars occur,[12] with the "population" and "deaths" counters increasing.
The ticker stops at the designated "years" value, at which point the world can be saved for use in any game mode. Should the player choose to retire a fortress, or should they be defeated, this world will persist and will become available for further games.
```

#### States (biomes)
For States: [Voronoi diagram](https://en.wikipedia.org/wiki/Voronoi_diagram)  

5 States (equivalent to a minecraft biome) with a specific civilisation each time (kinda like Horizon zero dawn) with each region having:  
* specific language
* specific colors
* specific behaviors?
* specific animals and ecosystems  

How big should a region be? Needs playtesting to see how much time is needed per area, and how much time should be spent in each region (fun wise)  

* Desert
* Snow
* Plains

#### Layouts
Each state will then be splitted into **layout types**
* Big rooms
* Normal rooms
* Small rooms
* Mostly corridors
* Caves (organic shapes rather than straight corridors)
* Outside world?

The layout assets will still be defined by the state but will allow for a more varied gameplay

#### World Building Process
###### States Creation  
1 - Place capitals  
*Maybe give more than 5 capitals to the Voronoi algo, to get a more complex map (some states will have 2 capitals)*  
2 - Compute Voronoi diagram to get each state bounds  
3 - Slightly change each capital position?  
*May be needed as the Voronoi split is visible*  
4 - Generate the state name  
5 - Choose the state's alphabet  
*Unicode char ranges*    
6 - Assign the state to one of the 5 predefined states style (Desert etc...)  
7 - Generate a name for the leader / king etc  
8 - Generate a quick story about the state (will be displayed when the player enters the state for the 1st time)  
###### Layout Creation
For each state use a simplex noise (faster, less artifacts than perlin) to subdivide the

###### Add Objects and NPCs

## Clients
#### PyGame  
Other one (main one?) using PyGame  
visual look must be constrained to a pixel art style for ease of development  
Max 16px*16px sprites recommended  
not aimed at a realistic look  

#### Curses  
One with a Colored CLI using curses (python wrapper around ncurses)  
https://jonasjacek.github.io/colors/ for terminal color list  
Uses Unicode chars for display variety:  
https://fr.wikipedia.org/wiki/Table_des_caract%C3%A8res_Unicode_(0000-0FFF)  
