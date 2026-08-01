import os
import socket
import struct
import pathlib

from google.protobuf import text_format
from robots import ourRobots, opponents
from misc.config import visionSettings as settings
import time

team = settings['team']
updateInterval = int(settings['updateInterval'])
useSavedData = bool(settings['useSavedData'])

if any(
        not os.path.exists('proto/' + proto + '_pb2.py')
        for proto in ('ssl_gc_referee_message', 'ssl_gc_common', 'ssl_gc_game_event', 'ssl_vision_wrapper')
):
    print("Compiling Protobuf files...")
    import grpc_tools.protoc
    grpc_tools.protoc.main([
        'protoc',
        '--python_out=.', '--pyi_out=.',
        *[str(path) for path in pathlib.Path().rglob('proto/*.proto')]
    ])

print("[VISION] Proto files compiled.")
from proto.ssl_vision_wrapper_pb2 import SSL_WrapperPacket

def open_multicast_socket(ip: str, port: int) -> socket.socket:
    # Adapted from https://stackoverflow.com/a/1794373 (CC BY-SA 4.0 by Gordon Wrigley)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Windows does not allow binding UDP sockets to a specific ip address.
    sock.bind(('' if os.name == 'nt' else ip, port))

    sock.setsockopt(
        socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
        struct.pack('4sl', socket.inet_aton(ip), socket.INADDR_ANY)
    )
    return sock

class visionClient:
    def __init__(self, ip: str, port: int):
        self.packet = SSL_WrapperPacket()
        self.sock = open_multicast_socket(ip, port)
        print("[VISION] Ready to receive.")

    def receive(self):
        data, address = self.sock.recvfrom(1024)
        print(data)
        # print(data.decode('utf-8'))
        packet = SSL_WrapperPacket()
        packet.ParseFromString(data)
        return packet

    def getVisionTest(self):
        with open("misc/vision_test.txt", "r") as f:
            text = f.read()

        packet = SSL_WrapperPacket()
        return text_format.Parse(text, packet)


def updateRobots(packet):
    if packet.HasField('detection'):
        onFieldRobots = []
        teamList = None
        onFieldOpps = []
        oppList = None
        if team == "yellow":
            teamList = packet.detection.robots_yellow
            oppList = packet.detection.robots_blue
        else:
            teamList = packet.detection.robots_blue
            oppList = packet.detection.robots_yellow

        for robot in teamList:
            id = str(robot.robot_id)
            onFieldRobots.append(robot.robot_id)
            ourRobots[id].position = (robot.x, robot.y)
            ourRobots[id].onField = True

            #print(f'[{team.upper()}] Robot {id} is at {ourRobots[id].position}')

        for robot in ourRobots:
            ourRobots[robot].onField = robot in onFieldRobots

        for robot in oppList:
            id = str(robot.robot_id)
            onFieldOpps.append(id)
            opponents[id].x = robot.x
            opponents[id].y = robot.y
            #print(f'[OPPS] Robot {id} is at {ourRobots[id].position}')


vision = visionClient(settings['ip'], int(settings['port']))

def activateVision():
    while True:
        if useSavedData:
            package = vision.getVisionTest()
        else:
            package = vision.receive()

        updateRobots(package)
        time.sleep(updateInterval)
