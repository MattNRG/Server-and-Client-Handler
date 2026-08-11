import threading
import colorama
from robots import addRobots
from vision import activateVision
from wifi import startServer, checkRobots
from commands import startCommands
from controller import controller

from colorama import Back
colorama.init(autoreset=True)

addRobots()
threading.Thread(target=activateVision, daemon=True).start()

print(Back.GREEN + "        READY TO START        ")
threading.Thread(target=startServer, daemon=True).start()
threading.Thread(target=checkRobots, daemon=True).start()
input()
threading.Thread(target=startCommands, daemon=True).start()

# Things that need to be done in main thread
while True:
    controller.update()
