import uuid
import socket
import socketserver
import time
import sys
import subprocess
import os

from classes.packet import Packet

block_size = 4096
nodes_dir = "dfs_data/data_nodes"

def usage():
	print(f"Usage: python3 data-node.py <server address> <port> <data path> <metadata port, default=8000>")
	sys.exit(0)

def register(meta_ip, meta_port, data_ip, data_port):

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Connecting to meta data server")
	s.connect((meta_ip, meta_port))

	try:
		packet = Packet()
		packet.buildDNPacket('reg', data_ip, data_port)
		s.sendall(packet.getEncodedPacket().encode())
		while True:
			response = s.recv(1024).decode()
			if not response:
				continue
			elif response == "DUP":
				print("Address and Port already registered.")
				break
			elif response == "ACK":
				print("Data node registered")
				break
	finally:
		print("Closing connection to meta_data server")
		s.close()

class DataNodeTCPHandler(socketserver.BaseRequestHandler):
	def handle_put(self, packet):
		print(" ") #TODO

	def handle_get(self, packet):
		print(" ") #TODO

	def handle(self):
		msg = self.request.recv(1024)
		print("Message received")

		p = Packet()
		p.decodePacket(msg)

		cmd = p.getCommand()
		if cmd == "put":
			self.handle_put(p)
		elif cmd == "get":
			self.handle_get(p)

if __name__ == '__main__':
	META_PORT = 8000    

	#Check to see if program is run with the correct amount of arguments
	if len(sys.argv) < 4:
		usage()
	
	try:
		HOST = sys.argv[1]
		PORT = int(sys.argv[2])
		DATA_NODE = sys.argv[3]

		if len(sys.argv) > 4:
			META_PORT = int(sys.argv[4])

	except:
		usage()

	if not os.path.isdir(nodes_dir): #If data nodes dir doest exist, make it
		print("Initalizing first data node")
		os.makedirs(f"{nodes_dir}/{DATA_NODE}", exist_ok=True)
	elif not os.path.isdir(f"{nodes_dir}/{DATA_NODE}"):
		print("Initializing data node")
		os.mkdir(f"{nodes_dir}/{DATA_NODE}")

	register("localhost", META_PORT, HOST, PORT)

    # Create the server
	with socketserver.TCPServer((HOST, PORT), DataNodeTCPHandler) as server:
		# Activate the server; this will keep running until you
		# interrupt the program with Ctrl-C
		server.serve_forever()
