import sys
import threading
import time

import colorama
from colorama import Fore, Back

from controller import setupPygame, running, disconnectPygame
from misc.config import robotSettings as settings, visionSettings, changeSetting
from robots import ourRobots, addRobots
from wifi import sendCommand

colorama.init(autoreset=True)

debug = False
robotAmount = int(settings['LoadRobots'])

helpText = """Welcome to the help menu! Currently available commands are:
active           -   Lists all active robots
map              -   Lists all robots on the map 
list <ROBOTID>   -   Lists all or specific robot(s) 
pos  <ROBOTID>   -   Displays the position of a specific robot ️
threads          -   Displays the amount of active threads
help             -   Shows this menu
exit             -   Ends the program
set <SETTING> <VALUE> -   Sets a setting
team              -   Displays the current team

Following commands are meant only for debugging purposes:
move <ROBOTID> <vX> <vY> <W> <Kicker?>  -   Moves a robot for 1000ms with the given parameters 
kick <ROBOTID> <Kicker?>                -   Turns on the kicker  
encont                                  -   Enables moving robots using Xbox Controller  
control <ROBOTID>                       -   Binds a controller to a robot                
decont                                  -   Disables moving robots using Xbox Controller
                                                                                          
Other:
quote                                   -   Displays a quote from RoboCup 2026
"""

quote = """We had 1 month to design it, 1 month to build it, and one month to debug it.
And that month was February
- Siim 2026"""

def getActiveRobots():
    print('ACTIVE ROBOTS')

    count = 0

    for robotid in range(robotAmount):
        robotClass = ourRobots[str(robotid)]
        if robotClass.connected:
            count += 1
            print(robotClass)

    if count == 0:
        print(Fore.YELLOW + 'No robots are connected')


def getMapRobots():
    print('ON MAP ROBOTS')

    count = 0

    for robotid in range(robotAmount):
        robotClass = ourRobots[str(robotid)]
        if robotClass.onMap:
            count += 1
            print(robotClass)

    if count == 0:
        print(Fore.YELLOW + 'No robots are on map')


def startCommands():
    time.sleep(.1)

    runningController = False

    print('[CMD] Console commands enabled, type "help" for more info')
    while True:
        try:
            command = input("[YOU]: ").lower()
            commandList = command.split()

            if debug:
                print(commandList)

            if len(commandList) == 0 or commandList[0] == "exit":
                print(Back.RED + "       PROCESS FINISHED       ")
                sys.exit()

            match commandList[0]:

                case 'hi':
                    print(Fore.LIGHTYELLOW_EX + "[CMD] hi")
                    continue

                case "active":
                    getActiveRobots()
                    continue

                case 'map':
                    getMapRobots()
                    continue

                case 'list':
                    if len(commandList) > 1:
                        robotClass = ourRobots[commandList[1]]
                        print(robotClass)
                        continue

                    for id in range(robotAmount):
                        robotClass = ourRobots[str(id)]
                        print(robotClass)
                    continue

                case 'move':
                    print(Back.RED + "THIS COMMAND IS NOT YET IMPLEMENTED")
                    sendCommand(commandList[1], int(commandList[2]), int(commandList[3]), int(commandList[4]), int(commandList[5]))
                    continue

                case 'kick':
                    print(Back.RED + "THIS COMMAND IS NOT YET IMPLEMENTED")
                    sendCommand(commandList[1], 0, 0, 0, 1)
                    continue

                case 'encont':
                    # Enables moving robots using Xbox Controller
                    if not runningController:
                        print(Back.LIGHTRED_EX + "THIS COMMAND IS BEING TESTED")
                        success = setupPygame()
                        if success:
                            runningController = True
                            running = True
                            # threading.Thread(target=getJoystick, daemon=True).start()
                            print(Back.GREEN + "[CONT] Controller successfully connected")
                    continue

                case 'decont':
                    if runningController:
                        disconnectPygame()
                        # Disables moving robots using Xbox Controller
                        print(Back.LIGHTRED_EX + "THIS COMMAND IS BEING TESTED")
                        disconnectPygame()
                        print("[CONT] Disconnected controller")
                    else:
                        print(Fore.RED + "[CMD] There is no controller connected")
                    continue

                case 'control':
                    # Binds a controller to a robot
                    print(Back.RED + "THIS COMMAND IS NOT YET IMPLEMENTED")
                    continue

                case "pos":
                    robotClass = ourRobots[commandList[1]]
                    position = robotClass.position
                    print(f'[CMD] Robot{commandList[1]} is at x: {position[0]} y: {position[1]}')
                    continue

                case 'threads':
                    print(f'There are {threading.active_count() - 1} additional threads')
                    continue

                case 'team':
                    print(f'Team is currently set as: {visionSettings["team"].upper()}')
                    continue

                case 'set':

                    match commandList[1]:
                        # Set commands
                        case 'team':
                            #print(Back.RED + "THIS COMMAND IS NOT YET IMPLEMENTED")
                            match commandList[2]:
                                case 'yellow':
                                    changeSetting("VISION", "team", "yellow")
                                    print(Fore.YELLOW + "[CMD] Team set to yellow")

                                    continue
                                case 'blue':
                                    changeSetting("VISION", "team", "blue")
                                    print(Fore.BLUE + "[CMD] Team set to blue")
                                    continue

                case 'quote':
                    print(quote)
                    continue

                case 'help':
                    print(helpText)
                    continue
            
            print('Invalid command, type "help" for more info')

        except IndexError as e:
            print(Fore.RED + f"[CMD] Missing 2. parameter, more info: {e}")

        except Exception as e:
            print(Fore.RED + f"[CMD] ERROR, cause: {e}")

print('[CMD] Console Commands Loaded')
if __name__ == "__main__":
    addRobots()
    startCommands()
