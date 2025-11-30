import socket
import sys

from classes.packet import Packet

def usage():
	print("Usage: python3 ls.py <server>:<port, default=8000>")
	sys.exit(0)

def client(ip, port):

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Connecting to meta data server")
	s.connect((ip, port))
	try:
		packet = Packet()
		packet.buildClientPacket("ls", [])
		s.sendall(packet.getEncodedPacket().encode())
		print("Sent ls request")
		while True:
			file_list = s.recv(1024).decode()
			if not file_list:
				continue
			print(f"\nDFS contents:\n{file_list}")
			break
	finally:
		print("Closing connection to meta_data server")
		s.close()

if __name__ == "__main__":
	if len(sys.argv) < 2:
		usage()


	ip = None
	port = 8000 
	server = sys.argv[1].split(":")
	if len(server) == 1:
		ip = server[0]
	elif len(server) == 2:
		ip = server[0]
		port = int(server[1])

	if not ip:
		usage()

	client(ip, port)
