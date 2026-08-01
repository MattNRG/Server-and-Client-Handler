import socket
import struct
import time
import threading
import random
from misc.config import wifiSettings as settings
from sensors import readOrientation

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
        client.send(struct.pack('B', 4))
        time.sleep(heartBeatInterval)

def sendOrientation():
    while connected:
        print('Sending orientation')
        orientation = readOrientation()
        print(orientation)
        client.send(struct.pack('Bi', 6, orientation))
        print(f"Sending orientation: {orientation}")
        time.sleep(rotationInterval)

def connect():
    global client, connected
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    connected = True
    print("Connected")

    # Needs confirmation, cuz robotid packet can be lost and orientation/heartbeat will be set as robotid
    client.send(robotid.encode())
    if not client.recv(1024).decode() == "OK":
        print("Robotid not confirmed")
        return

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