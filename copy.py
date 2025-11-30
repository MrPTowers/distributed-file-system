import socket
import sys
import os

from classes.packet import Packet
from classes.dnode import DataNode

block_size = 4096

def usage():
	print("Usage: python3 copy.py <server>:<port>:<dfs file path> <destination file>\nor\npython3 copy.py <source file> <server>:<port>:<dfs file path>")
	sys.exit(0)

def copyToDFS(address, file_name, path):

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Connecting to metadata server")
	s.connect(address)
	try:
		file_size = os.path.getsize(path)
		packet = Packet()
		if os.path.isdir(file_name):
			file_list = os.listdir(file_name)
			packet.buildClientPacket("put", [path, file_size, file_list])
			s.sendall(packet.getEncodedPacket().encode())
			print("Sent put request")
		else:
			packet.buildClientPacket("put", [path, file_size])
			s.sendall(packet.getEncodedPacket().encode())
			print("Sent put request")
		rec_packet = Packet()
		while True:
			msg = s.recv(1024).decode()
			if not msg:
				continue
			rec_packet.decodePacket(msg)
			print(rec_packet.getData())
			break

	finally:
		print("Closing connection to meta_data server")
		s.close()


		#Connect to data nodes and split message into 4KB blocks

	return 0

def copyFromDFS(address, file_name, path):
	
	#Connect to md server
		#if the file exists, receive packet with array of block ids and data nodes

	#For loop over all dnodes collecting blocks in order and inserting contents into new file with specified name

	return 0

if __name__ == "__main__":
	if len(sys.argv) < 3:
		usage()

	file_from = sys.argv[1].split(":")
	file_to = sys.argv[2].split(":")

	print(file_from)
	print(file_to)

	if len(file_from) > 1:

		ip = file_from[0]
		port = int(file_from[1])
		from_path = file_from[2]
		to_path = sys.argv[2]

		copyFromDFS((ip, port), from_path, to_path)

	elif len(file_to) > 2:
		ip = file_to[0]
		port = int(file_to[1])
		to_path = file_to[2]
		from_path = sys.argv[1]
		print(from_path)

		if os.path.exists(from_path):
			copyToDFS((ip, port), to_path, from_path)
		else:
			print("File does not exist")
