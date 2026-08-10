import socket
import threading
import struct
import time
import colorama
from colorama import Fore, Back
colorama.init(autoreset=True)
from robots import ourRobots
from misc.config import wifiSettings as settings
from misc import config as notify

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((settings['ip'], int(settings['port'])))  # Listening on everything

heartBeatTime = int(settings['heartBeatTime'])
checkHeartbeat = int(settings['checkHeartbeat'])

def unpack(packet, robotClass):

    # 1 Send commands
    # 2 Get info
    # 3 Set params
    # 4 Heartbeat
    # 5 Stop all
    # 6 Info [Auto DATA]
    # 7 Message
    #print(f'[DEBUG] Packet: {packet}')

    packetType = packet[0]
    robotClass.lastSeen = time.time()
    match packetType:  # Can be expanded later
        case 2:
            # Will we replaced with other info
            packetType, battery, gyroRotation = struct.unpack('BBB', packet)
            robotClass.battery = battery
            robotClass.gyroRotation = gyroRotation
        case 4:
            packetType, battery, temp = struct.unpack('BBB', packet)
            robotClass.battery = battery
            robotClass.temperature = temp
            robotClass.lastSeen = time.time()
        case 6:
            packetType, rotation = struct.unpack('Bi', packet)
            robotClass.rotation = rotation
            print(f'[ROBOT {robotClass.id}] Rotation: {rotation}')
        case 7:
            print(f'[ROBOT {robotClass.id}] {packet.decode()}')
            pass

def checkRobots():
    # Basically heartbeat monitor so robo can connect again
    while True:
        # print(ourRobots)
        for robotID in list(ourRobots):
            # print(f"Checking {robotID}")
            robotClass = ourRobots[robotID]

            if time.time() - robotClass.lastSeen > heartBeatTime and robotClass.connected:
                print(Back.RED + f'[WI-FI] Disconnecting {robotID} due to inactivity')
                robotClass.disconnect()
        time.sleep(checkHeartbeat)


def handleRobot(robotid):
    robotClass = ourRobots[robotid]
    while True:
        try:
            message = robotClass.getMessage()

            unpack(message, robotClass)

            if message == "end" or message == "":
                break

        except Exception as Error:
            print(Back.RED + f'Ending thread due to {Error}')
            break

    if not robotClass.connected:
        return
    robotClass.disconnect()
    print(Fore.YELLOW + "[SERVER] Ending thread")


def startServer():
    try:
        print(Fore.LIGHTRED_EX + f"Server IP: {socket.gethostbyname(socket.gethostname())}")
        server.listen()
        while True:
            client, addr = server.accept()

            robotid = client.recv(1024).decode()
            print(robotid)
            client.send('OK'.encode())

            if ourRobots[robotid].connected:
                ourRobots[robotid].socket.close()

            ourRobots[robotid].lastSeen = time.time()
            ourRobots[robotid].connected = True
            ourRobots[robotid].addr = addr
            ourRobots[robotid].socket = client

            notify.message(f"[WI-FI] ROBOT {robotid} connected", f'IP: {addr[0]}')
            print(Back.GREEN + f'[WI-FI] ROBOT {robotid} connected IP: {addr[0]}')

            thread = threading.Thread(target=handleRobot, args=robotid, daemon=True)
            thread.start()
            print(f"[SERVER] Currently {threading.active_count() - 4} connection threads active")
    except Exception as Error:
        print(Fore.RED + f'[SERVER] {Error}')
