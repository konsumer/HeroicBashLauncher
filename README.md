# HeroicBashLauncher

Ever wanted to launch your EGS games installed through [Heroic Games Launcher](https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher) directly from the terminal, Lutris or any other frontend game launcher?
Heroic Bash Launcher lets you this very easily. 

You can now launch your game directly without having to open Heroic at all. There's no need to run `heroic` to find the game's launch command or write your own launch script with [legendary](https://github.com/derrod/legendary)! Thus saving your time!


![Heroic Bash Launcher](https://user-images.githubusercontent.com/74495920/142615495-a4e5e811-7ee3-41b8-ae80-d6d008820f2a.png)


## Pre-requisites
- Heroic Games Launcher 1.10 'Kizaru'
- Python 3
- Git


## Working

Heroic Bash Launcher automatically detects installed games and creates a launch file for each game. The launch file is created using the *bash shell script*, i.e. `.sh` files. For example, if I have Rocket League installed, it will create the launch file titled "Sugar.sh".

**For now, all launch files will be titled according to how legendary names the games (AppName.sh). The game's actual name will be mentioned in the launch file, as seen below.**

Every game's launch file will contain all the launch parameters according to the game's setting in Heroic Games Launcher, including cloud syncing for supported games. Here's an example below of "Sugar.sh" -

```
#!/bin/bash

#Game Name = Rocket League®


PULSE_LATENCY_MSEC=60 WINE_FULLSCREEN_FSR=1 WINE_FULLSCREEN_FSR_STRENGTH=1 WINEESYNC=1 MANGOHUD=1 /usr/bin/gamemoderun /opt/Heroic/resources/app.asar.unpacked/build/bin/linux/legendary launch Sugar --wine '/home/redromnon/.local/share/lutris/runners/wine/lutris-ge-6.21-1-x86_64/bin/wine64' --wine-prefix '/home/redromnon/.wine' || echo "NO INTERNET CONNECTION. Running game in offline mode..." && PULSE_LATENCY_MSEC=60 WINE_FULLSCREEN_FSR=1 WINE_FULLSCREEN_FSR_STRENGTH=1 WINEESYNC=1 MANGOHUD=1 /usr/bin/gamemoderun /opt/Heroic/resources/app.asar.unpacked/build/bin/linux/legendary launch Sugar --offline --wine '/home/redromnon/.local/share/lutris/runners/wine/lutris-ge-6.21-1-x86_64/bin/wine64' --wine-prefix '/home/redromnon/.wine'
```

All these launch files will be available in the **GameFiles** folder. 


## Usage

First, download and extract the project folder by clicking on the green button "Code" and hit "Download Zip". Or use Git to clone.


### Running the Program
Using your terminal, navigate to this directory (~/HeroicBashLauncher) and execute the program by running the following command `./HeroicBashLauncher.sh` or simply double-click this file. 
You will be required to enable executable permissions for this file.

**Keep in mind, you have to run this program everytime you change the Settings in the Heroic Games Launcher app. This helps to overwrite the old launch parameters with the new ones.**


### Running Games
You can execute a game's launch file using the terminal like ```./Sugar.sh``` or your preferred game launcher/manager like Lutris or EmulationStation.


### Updating the Program
Again using your terminal, navigate to this directory and run the command `git pull` to get the latest changes.


## Features Planned

- Name files according to the actual game name
- Ask user for a default path for saving game launch files
- Only update game launch files whose setting is changed
- Additional game launch options support (Eg. ARK)
- Automatically update launch parameters when executing game launch file


## Issues
Feel free to report any!


## Changelog

- Version 1.0 - 18/11/21
- Version 1.0.1 - 18/11/21

  - *Now detects if no games are installed and displays a relevant message.*  

- Version 1.1 - 20/11/21

  - *Launch files of uninstalled games won't be generated due to left over files.* 
  - *The game's actual name will be displayed and mentioned in the bash script.*

- Version 1.2 - 25/11/21

  - *Games now run in offline mode if no internet connection is detected.* 
  - *The save path is also included in the cloud save-sync parameter.* 
  - *The program ends execution after an interval of 2 sec.*


## License
This project is under the GNU GPLv3 license. You can take a look at the LICENSE.md for more information.
