import socket
import struct
import threading
import time
import random
from misc.config import wifiSettings as settings

roboID = random.randint(0, 11).__str__()
client = None
connected = False
ip = settings['ip']
port = int(settings['port'])
print(f"Current IP: {socket.gethostbyname(socket.gethostname())}")

def sendMessage(message):
    return struct.pack(f'BB{len(message)}s', 7, len(message), message.encode())

def heartBeat():
    while connected:
        client.send(struct.pack('B', 4))
        time.sleep(1)
    print("heartbeat stopped")


while True:
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        connected = True
        print("Connected")
        client.send(roboID.encode())
        thread = threading.Thread(target=heartBeat).start()
        while connected:
            message = input("What to send: ")
            client.send(sendMessage(message))
            if message == "end":
                connected = False
                print("Closing connection")
                client.close()
                time.sleep(3)
    except Exception as r:
        print(f"{r}; retrying..")
        time.sleep(2)