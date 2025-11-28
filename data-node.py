import uuid
import socket
import socketserver
import time
import sys
import subprocess

from classes.dnode import DataNode
from classes.packet import Packet

def usage():
	print(f"Usage: python3 data-node.py <server address> <port> <data path> <metadata port,default=8000")
	sys.exit(0)

def register(meta_ip, meta_port, data_ip, data_port):

	socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Connecting to meta data server")
	socket.connect((meta_ip, meta_port))

	try:
		response = "NAK"
		sp = Packet()
		while response == "NAK":
			sp.BuildSendPacket(data_ip, data_port)
			socket.sendall(packet.getEncodedPacket())
			if response == "DUP":
				print("DUP")
			elif response ==  "NAK":
				print("Error")
	finally:
		print("Closing connection to meta_data server")
		socket.close()


class DataNodeTCPHandler(socketserver.BaseRequestHandler):
	def handle_put(self, packet):
		print(" ") #TODO

	def handle_get(self, packet):
		print(" ") #TODO

	def handle(self):
		msg = self.request.recv(1024)
		print(" ") 

		#TODO

		p = Packet()
		p.decodePacket(msg)

		cmd = p.packet.cmd
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
		DATA_PATH = sys.argv[3]

		if len(sys.argv > 4):
			META_PORT = int(sys.argv[4])

		if not os.path.isdir(DATA_PATH):
			print(f"Error: Data path DATA_PATH{} is not a directory.")
			usage()
	except:
		usage()

	register("localhost", META_PORT, HOST, PORT)
	server = socketserver.TCPServer((HOST, PORT), DataNodeTCPHandler)

    # Create the server, binding to localhost on port 8000
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
