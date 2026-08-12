import struct

# 1 Send commands (4 bytes) BBBB
# 2 Get info
# 3 Set params
# 4 Heartbeat (3 bytes)
# 5 Stop all (1 byte)
# 6 Info [Auto DATA] (6 bytes)
# 7 Message (Auto scaling)
# print(f'[DEBUG] Packet: {packet}')

packetSizes = {
    4:  3,
    6:  5
}

def encodeHeartbeat(currentBattery, Temperature):
    return struct.pack('<BBB', 4, currentBattery, Temperature)

def encodeData(Orientation):
    return struct.pack('<Bi', 6, Orientation)

