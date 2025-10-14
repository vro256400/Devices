import socket

def getPwServer():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try :
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(b"srv_discovery", ("255.255.255.255", 7778))
        sock.settimeout(1) # 1 seconds
        data, address = sock.recvfrom(4096)
        return str(address)
    except Exception as e:
        return None
    finally:
        sock.close()
    

    