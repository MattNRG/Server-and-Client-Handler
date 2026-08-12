import socket


class Robot:
    def __init__(self):
        self.socket = None
        self.connected = False

        self.vx = 0
        self.vy = 0
        self.w = 0
        self.kicker = 0

    def getMessage(self):
        packet = self.socket.recv(1024)
        return packet

    def send(self, packet):
        self.socket.send(packet)

    def update(self, vx, vy, w, kicker):
        self.vx = vx
        self.vy = vy
        self.w = w
        self.kicker = kicker

    def disconnect(self):
        self.connected = False
        self.socket.close()
        self.socket = None


robotClass = Robot()