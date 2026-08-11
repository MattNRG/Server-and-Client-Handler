import socket
import threading
import struct
import time
import colorama
from colorama import Fore, Back
from robots import ourRobots
from misc.config import wifiSettings as settings
from misc import config as notify

colorama.init(autoreset=True)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((settings['ip'], int(settings['port'])))  # Listening on everything

heartBeatTime = int(settings['heartBeatTime'])
checkHeartbeat = int(settings['checkHeartbeat'])

# 1 Send commands
# 2 Get info
# 3 Set params
# 4 Heartbeat
# 5 Stop all
# 6 Info [Auto DATA]
# 7 Message
# print(f'[DEBUG] Packet: {packet}')

packetSizes = {
    4:  3,
    6:  5
}

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
            pass
        case 4:
            packetType, battery, temp = struct.unpack('<BBB', packet)
            robotClass.battery = battery
            robotClass.temperature = temp
        case 6:
            packetType, rotation = struct.unpack('<Bi', packet)
            robotClass.rotation = rotation
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
    buffer = b''
    while True:
        try:
            message = robotClass.getMessage()

            if message == "end" or message == "":
                break

            # Since there byte stream is causing issues we need to buffer the packets
            buffer += message

            while len(buffer) >= 1:
                packetType = buffer[0]
                packetSize = packetSizes.get(packetType)

                if packetSize is None:
                    print(f"[ROBOT {robotid}] Unknown packet type: {packetType}")
                    buffer = buffer[1:]
                    continue

                if len(buffer) < packetSize:
                    break

                packet = buffer[:packetSize]
                buffer = buffer[packetSize:]

                unpack(packet, robotClass)

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

            while True:
                try:
                    robotid = client.recv(1024).decode()
                    if type(int(robotid)) == int:
                        client.send('OK'.encode())
                        print('OK!')
                        break
                    client.send('NO'.encode())

                except Exception as Error:
                    print(f"[SERVER] Error whilst getting Roboid: {Error}")

            if ourRobots[robotid].connected:
                ourRobots[robotid].socket.close()

            ourRobots[robotid].lastSeen = time.time()
            ourRobots[robotid].connected = True
            ourRobots[robotid].addr = addr
            ourRobots[robotid].socket = client

            notify.message(f"[WI-FI] ROBOT {robotid} connected", f'IP: {addr[0]}')
            print(Back.GREEN + f'[WI-FI] ROBOT {robotid} connected IP: {addr[0]}')

            threading.Thread(target=handleRobot, args=(robotid,), daemon=True).start()
            print(f"[SERVER] Currently {threading.active_count() - 4} connection threads active")
    except Exception as Error:
        print(Fore.RED + f'[SERVER] {Error}')
