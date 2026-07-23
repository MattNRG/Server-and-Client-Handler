import socket
import struct
import threading
import time

roboID = "0"
client = None
connected = False
print(f"Current IP: {socket.gethostbyname(socket.gethostname())}")


def sendMessage(message):
    return struct.pack(f'BB{len(message)}s', 7, len(message), message.encode())

def heartBeat():
    while connected:
        client.send(struct.pack('B', 4))
        time.sleep(1)


while True:
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 9997))
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
    except ConnectionRefusedError as r:
        print(f"{r}; retrying..")
        time.sleep(1)