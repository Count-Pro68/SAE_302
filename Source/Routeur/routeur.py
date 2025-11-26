"""
**************
Code Broadcast
**************
"""
import socket

def discover_master(port=9000):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(2)

    message = b"WHO_IS_MASTER"
    s.sendto(message, ("<broadcast>", port))

    try:
        data, addr = s.recvfrom(1024)
        if data.startswith(b"MASTER_IP="):
            return data.decode().split("=")[1]
    except:
        pass

    return None
