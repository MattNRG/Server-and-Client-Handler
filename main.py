import threading
import colorama
from robots import addRobots
from vision import activateVision
from communication import startServer, checkRobots

from colorama import Back, Fore
colorama.init(autoreset=True)

addRobots()
threading.Thread(target=activateVision, daemon=True).start()

print(Back.GREEN + "        READY TO START        ")
threading.Thread(target=startServer, daemon=True).start()
threading.Thread(target=checkRobots, daemon=True).start()
input("ENTER TO CLOSE ALL THREADS")
print(Back.RED + "       PROCESS FINISHED       ")