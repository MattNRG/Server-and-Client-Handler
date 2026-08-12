import colorama
import struct
from colorama import Fore
from misc.config import robotSettings as settings
colorama.init(autoreset=True)

ourRobots = {}
opponents = {}
LoadRobots = int(settings['LoadRobots'])

class Ball:
    def __init__(self):
        self.position = (0, 0)


ball = Ball()

class OppRobot:
    def __init__(self, robotid):
        self.id = robotid
        self.position = (0, 0)
        self.onMap = False

    def __repr__(self):
        return f"Opponent {self.id} is on map: {self.onMap}, position: {self.position}"


class Robot:
    def __init__(self, robotid):
        self.id = robotid
        self.addr = (0, 0)
        self.socket = None
        self.lastSeen = 0
        self.connected = False

        self.onMap = False
        self.position = (0, 0)
        self.rotation = 0
        self.battery = 100
        self.gyroRotation = 0  # Don't remember what the plan with this was

        self.temperature = 10

    def __repr__(self):
       # return f"Robot {self.id} {self.addr[0]}, battery: {self.battery}, gyro: {self.gyroRotation}, on field map: {self.position}"
        info = (f""" [Robot {self.id}]
        IP: {self.addr[0]}
        Battery: {self.battery}
        Temperature: {self.temperature}
        Rotation: {self.rotation}*
        Position: x: {self.position[0]}, y: {self.position[1]}
        On Map: {self.onMap}
        Connection: {self.connected}
        Last Seen: {self.lastSeen}
        """)
        return info

    def getMessage(self):
        return self.socket.recv(1024)

    def sendCommands(self, vx, vy, w, kicker):
        package = struct.pack('BBBBB', 1, vx, vy, w, kicker)
        self.socket.send(package)

    def setParams(self, section, setting, value):
        pass

    def stop(self):
        package = struct.pack('B', 5)

    def getInfo(self):
        package = struct.pack('B', 2)

    def disconnect(self):
        self.socket.send(('end').encode())
        self.connected = False
        self.addr = (0, 0)
        self.socket.close()
        print(Fore.YELLOW + f"[ROBOT {self.id}] {self.addr[0]} disconnected")


def addRobots():
    for i in range(LoadRobots):
        robotID = str(i)
        robotClass = Robot(robotID)
        ourRobots[robotID] = robotClass

        oppsClass = OppRobot(robotID)
        opponents[robotID] = oppsClass

    print('[ROBOTS] Robots loaded successfully')
