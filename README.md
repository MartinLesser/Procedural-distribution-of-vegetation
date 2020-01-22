# Procedural distribution of vegetation
Author: Martin Lesser

Source code of my procedural distribution system for my master thesis with the title 
"Procedural distribution of vegetation on a heightmap-based terrain".
The application calculates the growth probability of a given vegetation type for every pixel on a given heightmap.
You can define maps, vegetation types, biom types and soil types via the GUI. All definitions and calculations will be 
stored and loaded when the application is started. 

The basis for the calculations are the heightmap of a terrain and its soil types map. The heightmap contains the
heights of every pixel at every point on the terrain. And the soil types map contains the soil ID at every point on the 
terrain. Based on these two maps the following calculations will be made:
- insolation of every pixel during one day (kilo calories at every pixel)
- geological relief of the terrain (normal vector at every pixel)
- amount of water at every pixel
- depth of soil at every pixel 

Depending on the vegetation type definition the probability for the growth will be calculated at every pixel.
All definitions (vegetation types, bioms etc.) can be done via UI or manually within the yaml files.

![appletrees_growth_probabilities_on_terrain](https://github.com/MartinLesser/Procedural-distribution-of-vegetation/blob/master/resources/screenshots/calculated_results_terrain_small_appletrees.png "Results of the calculation for the growth probability of appletrees on a terrain")  
You can find more screenshots at [resources/screenshots](resources/screenshots)

## Dependencies
Linux needs additional packages to be installed:
- python3-dev
- python3-tk
### Needed pip modules
Babel >= 2.7.0  
Image >= 1.5.27  
imageio >= 2.5.0  
matplotlib >= 3.1.1  
numpy >= 1.17.0  
psutil >= 5.6.3  
pytz >= 2019.1  
pyyaml >= 5.1.1  
tkfilebrowser >= 2.3.1  
pywin32 (for windows)

## Definitions
Vegetation type definition:
- name
- energy demand (kcal per day)
- soil type demand
- soil depth demand (cm)
- water demand (liter per day)

Soil type definition:
- name
- ID (the soil map contains the IDs. The ID at a pixel states which soil type it is.)
- albedo (how much light is reflected by the ground. percentage as a fraction)
- water absorption (percentage as a fraction)

Biom type definition:
- name
- atmospheric absorption (percentage for how much light the atmosphere absorps)
- atmospheric diffusion (percentage for how much light gets diffused by the atmosphere)
- average rainfall per day (liter)
- cloud reflection (percentage for how much light gets reflected by clouds)
- groundwater (how much liter water there is per square meter)

Map definition:
- name
- biom (see above)
- height conversion (this value is used to convert the values of the height map to actual height values. e.g. a value of
0.1 would mean the height was sampled with a precision of 10 cm)
- heightmap path (path to the heightmap image)
- maximal soil depth (the soil depth of every pixel will be calculated depending on the max soil depth and the local
rise)
- pixel size (resolution of the terrain in meter. e.g. 15 would mean 1 pixel covers 15m of the terrain)
- texture map path (path to the soil image)

## How to use
You have to compile the project and execute the main file that can be found at [intern/src/python/Logic/main.py](intern/src/python/Logic/main.py).

## Further information
If you want more information how the system works you could read my master thesis (see [doc directory](doc/))
which is written in german. If you can't understand german you can send me an email and I can expand
this readme.

## Known bugs
The GUI works best with Windows. It also works with Ubuntu and MacOS but the interface can be buggy. Especially for
Ubuntu the GUI sometimes won't show up, you have to minimize and maximize the window to make the GUI visible.

## Possible improvements
The underlying model for the probability calculations could be more realistic. The project was only made for games in
mind. And for that it can be sufficient. But to use this application for real world problems the model has to be 
improved and advanced.
There is also a resolution problem. If the pixel resolution size is greater or smaller than one square meter the 
calculations for every pixel will nevertheless be done as if it were only one square meter.