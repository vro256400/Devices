import socket
import sys

if (len(sys.argv) != 2):
	print ("exitDevScrypt.py <device ip>")
ip = sys.argv[1]

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((ip, 9999))

command = bytes('E', "utf-8")
clientsocket.send(command)