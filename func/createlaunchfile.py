#Creates the launch script and additional flatpak launch script for launching games

import os, sys, json
from func import configpath
from func.checkparameters import checkparameters
from func.gameName import filegamename
from func.steam import addtoscript, addtosteam

def createlaunchfile(gamename, appname, gamejson, gametype):

    #Store the game's total no. of plays
    with open(configpath.timestamppath, encoding='utf-8') as t:
        gametimestamp = json.load(t)

    #Check if the game has been launched atleast once from Heroic, otherwise set it to 0.
    try:
        totalgameplays = gametimestamp[appname]["totalPlayed"]
    except:
        totalgameplays = '0'
    
    # Check/Update parameters
    gamecommand = checkparameters(appname, gamejson, gametype) # returns launchcommand, offline_launchcommand, cloudsync
    cloudsync = gamecommand[2]
    
    #Generating game's file name
    simplified_gamename = filegamename(gamename)

    #Set file paths
    if "GameFiles" in os.getcwd():#select parent dir
        executablepath = os.path.dirname(os.getcwd()) + '/HeroicBashLauncher' + ' "' + gamename + '" "' + appname + '" "' + gamejson + '" "' + gametype + '"' 
        gameFilepath = os.getcwd() + "/" + simplified_gamename + ".sh"
        flatpakgamescriptpath = os.getcwd() + "/launchflatpakgame.sh"
    else:#launching from setup.sh
        executablepath = os.getcwd() + '/HeroicBashLauncher' + ' "' + gamename + '" "' + appname + '" "' + gamejson + '" "' + gametype + '"'
        gameFilepath = os.getcwd() + "/GameFiles/" + simplified_gamename + ".sh"
        flatpakgamescriptpath = os.getcwd() + "/GameFiles/launchflatpakgame.sh"
    
    #Launch commands for flatpak
    if configpath.is_flatpak == False:
        launchflatpakgame = ''
        showlaunchcommand = ''
    else:
        launchflatpakgame = 'flatpak run --command=./launchflatpakgame.sh com.heroicgameslauncher.hgl' 
        showlaunchcommand = '#Launch Command\n    #' + gamecommand[0]#Left space for alignment

    ####################################################################################################################
    #Launch Script Format
    launch_script = ("""#!/bin/bash 

    #Generate log
    exec > logs/{logname}.log 2>&1

    #Enable UTF-8 Encoding
    export LC_ALL=en_US.UTF-8

    #Game Name = {game_name} ({game_type}) 

    #App Name = {app_name}

    #Override launch parameters
    {executable_path}

    #Total Plays
    totalplays={totalplays}

    #Check if game is newly installed
    if [[ $totalplays -eq 0 ]] 
    then
        echo "This looks like a newly installed game. Please launch the game once from Heroic to avoid issues using Bash Launcher"
        zenity --warning --title="Process Paused" --text="This looks like a newly installed game\n\nPlease launch the game once from Heroic to avoid issues using Bash Launcher" --width=400 --timeout=8
    fi

    {launch_game_in_flatpak}

    {show_launch_command}

    """).format(logname = simplified_gamename,game_name = gamename, game_type = gametype, app_name = appname, 
                executable_path = executablepath, launch_game_in_flatpak = launchflatpakgame, 
                show_launch_command = showlaunchcommand, totalplays = totalgameplays)

    
    #Flatpak Game Script Format
    launch_flatpak_script = ("""#!/bin/bash

    #Currently created launch script for {game_name} ({app_name}) ({game_type})
    #Launches from {gamelaunchscript}.sh


    """).format(game_name = gamename, game_type = gametype, app_name = appname, gamelaunchscript = simplified_gamename)


    
    #Epic Games Format (Track wineserver before running post-game sync)
    epic_script = ("""

    #Launch game
    {savesync}

    ({launchcommand} || (echo "---CANNOT CONNECT TO NETWORK. RUNNING IN OFFLINE MODE---" ; {offline_launchcommand})) || (zenity --error --title="Error" --text="Failed to launch {game_name}\n\nPlease check the game log under GameFiles/logs/ in the HeroicBashLauncher folder for the error and consider reporting it as an issue on GitHub." --width=200; exit)

    #Wait for game to launch
    sleep 10
    
    while [ 1 ]
    do

        checkwine="wineserver"

        if pgrep -x "$checkwine" >/dev/null
        then
            :
        else
            echo "$checkwine stopped"
            echo "{game_name} stopped"
            {savesync}
            exit 
        fi

        sleep 3
    done

    """).format(launchcommand = gamecommand[0], offline_launchcommand = gamecommand[1], 
                savesync = cloudsync, game_name = gamename)

    
    #GOG format (without cloud sync check)
    gog_script = ("""

    #Launch game
    ({launchcommand} || (echo "---CANNOT CONNECT TO NETWORK. RUNNING IN OFFLINE MODE---" ; {offline_launchcommand})) || (zenity --error --title="Error" --text="Failed to launch ' + {game_name} + '\n\nPlease check the game log under GameFiles/logs/ in the HeroicBashLauncher folder for the error and consider reporting it as an issue on GitHub." --width=200; exit)

    """).format(launchcommand = gamecommand[0], offline_launchcommand = gamecommand[1], game_name = gamename) 

    ####################################################################################################################
    #Create final launch script depending on gametype
    if configpath.is_flatpak == False:
        if gametype == "epic":
            final_launch_script = launch_script + epic_script
        else:
            final_launch_script = launch_script + gog_script
    else:
        
        final_launch_script = launch_script
        
        if gametype == "epic":
            flatpak_launch_script = launch_flatpak_script + epic_script 
        else:
            flatpak_launch_script = launch_flatpak_script + gog_script 
    
    
    #Write to file
    with open(gameFilepath, "w") as f:
            f.write(final_launch_script)
    os.system("chmod u+x " + gameFilepath)

    if configpath.is_flatpak == True:

        with open(flatpakgamescriptpath, "w") as f:
            f.write(flatpak_launch_script)
        os.system("chmod u+x " + flatpakgamescriptpath)
    
    
    #If system is Steam Deck, add to Steam right away or add to Steam script
    if "deck" in os.path.expanduser("~"):
        addtosteam(gamename)
    else:
        addtoscript(gamename)