import socket


class Robot:
    def __init__(self):
        self.socket = None
        self.connected = False

        self.vx = 0
        self.vy = 0
        self.w = 0
        self.kicker = 0

    def recieve(self):
        pass

    def sendPacket(self, packet):
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