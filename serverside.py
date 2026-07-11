import socket
import struct
import threading
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999))  # Listening on ethernet, wifi and loopback

# Super proud of this
class Robot:
    def __init__(self, robotid, addr, socket):
        self.id = robotid
        self.addr = addr
        self.socket = socket
        self.lastSeen = time.time()
        self.active = True

        self.position = (0,0)
        self.rotation = 0
        self.battery = 100

# Packet handleres unfinished
packets = {
    #1: ('FORMAT', connectRobot),
    #2: ('FORMAT', sendCommands),
    #3: ('FORMAT', getInfo),
    #4: ('FORMAT', setParams),
    #5: ('FORMAT', heartbeat),
    #6: ('FORMAT', stopAll),
}

currentRobots = {}
# Format, robotID: (IP, PORT), TIME, SOCKET, ACTIVE
# RobotID, TUPLE [0], TIME [1], SOCKET [2], ACTIVE [3]

heartBeatTime = 10

def disconnectRobot(robotClass):
    print(f"Robot{robotClass.id}: {robotClass.addr[0]} disconnected")
    # currentRobots[robotID][3] = False
    robotClass.socket.close()
    del currentRobots[robotClass.id]


def checkRobots():
    # Basically heartbeat monitor so robo can connect again
    while True:
        print(currentRobots)
        for robotID in list(currentRobots):
            print(f"Checking {robotID}")
            robotClass = currentRobots[robotID]

            if time.time() - robotClass.lastSeen > heartBeatTime:
                print(f'Removing {robotClass.id} due to inactivity')
                disconnectRobot(robotClass)
        time.sleep(1)

def connectRobot(client, addr, robotID):
    robotClass = Robot(robotID, addr, client)
    currentRobots[robotID] = robotClass
    print(currentRobots)
    return robotClass

def handleClient(robotid):
    robotClass = currentRobots[robotid]
    print("Connected by: ", robotClass.addr[0])
    while True:
        try:
            #messageType = client.recv(1024).decode()
           #messageType = int(messageType)
            message = robotClass.socket.recv(1024).decode()
            print(f"{robotClass.addr[0]}: {message}")
            robotClass.lastSeen = time.time()

            if message == "end":
                break
        except:
            break
    if not robotClass.active: return
    disconnectRobot(robotClass)

def startServer():
    print(f"Server created - IP: {socket.gethostbyname(socket.gethostname())}")
    server.listen()
    while True:
        client, addr = server.accept()
        print("New ROBOT connected")

        roboid = client.recv(1024).decode()
        robotClass = connectRobot(client, addr, roboid)

        thread = threading.Thread(target=handleClient, args=(roboid), daemon=True)
        thread.start()
        print(f"Currently {threading.active_count() - 2} connection threads active")

threading.Thread(target=startServer, daemon=True).start()
threading.Thread(target=checkRobots(), daemon=True).start()
input("Press enter to stop")