import socket

serverIp = None

def getPwServer():
    global serverIp
    if serverIp != None:
        return serverIp

    print("Server discovery")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try :
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(b"srv_discovery", ("255.255.255.255", 7778))
        sock.settimeout(1000) # 1 seconds
        data, address = sock.recvfrom(4096)
        serverIp = str(address[0])
        print("Pw server detected ip =", serverIp)
        return serverIp
    except Exception as e:
        return None
    finally:
        sock.close()
    

    