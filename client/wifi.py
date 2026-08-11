import socket
import struct
import time
import threading
import random
from math import fabs

from misc.config import wifiSettings as settings
from sensors import readOrientation, currentBattery, temperature

connected = False
client = None
robotid = random.randint(0, 11).__str__()

ip = settings['ip']
port = int(settings['port'])
heartBeatInterval = int(settings['heartBeatInterval'])
rotationInterval = float(settings['rotationInterval'])

def sendMessage(message):
    return struct.pack(f'BB{len(message)}s', 7, len(message), message.encode())

def heartBeat():
    while connected:
        package = struct.pack('<BBB', 4, currentBattery, temperature)
        client.send(package)
        time.sleep(heartBeatInterval)   

def sendOrientation():
    while connected:
        print('Sending orientation')
        orientation = readOrientation()
        print(orientation)
        package = struct.pack('<Bi', 6, orientation)
        client.send(package)
        print(f"Sent orientation: {orientation}")
        time.sleep(rotationInterval)

def connect():
    global client, connected
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    print("Connected")

    # Needs confirmation, cuz robotid packet can be lost and orientation/heartbeat will be set as robotid
    while True:
        client.send(robotid.encode())
        receive = client.recv(1024).decode()
        print(receive)
        if receive == "OK":
            break

        print("Robotid not confirmed")

    connected = True
    threading.Thread(target=heartBeat).start()
    threading.Thread(target=sendOrientation).start()
    while connected:
        message = input("What to send: ")
        client.send(sendMessage(message))
        if message == "end":
            connected = False
            print("Closing connection")
            client.close()
            time.sleep(3)