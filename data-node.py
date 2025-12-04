import uuid
import socket
import socketserver
import sys
import os
import json

from classes.packet import Packet

block_size = 4096
nodes_dir = "dfs_data/data_nodes"

def usage():
	print(f"Usage: python3 data-node.py <server address> <port> <data path> <metadata port, default=8000>")
	sys.exit(0)

def recv_json(conn):
	buf = b""
	while True:
		chunk = conn.recv(4096)
		if not chunk:
			break
		buf += chunk

		try:
			text = buf.decode()
			json.loads(text)	# Check if JSON is complete
			return text		# Valid JSON → return it
		except json.JSONDecodeError:
			continue			# Not complete → keep reading
		except UnicodeDecodeError:
			continue

	return None

def register(meta_ip, meta_port, data_ip, data_port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Connecting to metadata server...")
	s.connect((meta_ip, meta_port))

	try:
		packet = Packet()
		packet.buildDNPacket('reg', data_ip, data_port)
		s.sendall(packet.getEncodedPacket().encode())

		while True:
			resp = s.recv(1024).decode().strip()
			if not resp:
				continue

			if resp == "ACK":
				print("Data node registered.")
				break
			elif resp == "DUP":
				print("Data node already registered.")
				break
			else:
				print("Unexpected response from metadata server:", resp)
				break

	finally:
		print("Closing connection to metadata server.")
		s.close()


class DataNodeTCPHandler(socketserver.BaseRequestHandler):
	def handle_put(self, packet):
		#Handle put request (from copy client)

		block_data = packet.getData()

		block_id = str(uuid.uuid4())
		block_path = f"{node_path}/{block_id}"
		with open(block_path, "wb") as block:
			block.write(block_data)

		res_packet = Packet()
		res_packet.buildMDPacket(block_id)
		self.request.sendall(res_packet.getEncodedPacket().encode())


	def handle_get(self, packet):
		#Handle get request (from copy client)
		block_id = packet.getData()

		node_dir = self.server.node_path
		block_path = f"{node_dir}/{block_id}"

		if not os.path.exists(block_path):
			res_packet = Packet()
			res_packet.buildMDPacket(None)
			self.request.sendall(res_packet.getEncodedPacket().encode())
			print(f"Block {block_id} not found.")
			return

		with open(block_path, "rb") as block:
			data = block.read()

		res_packet = Packet()
		res_packet.buildMDPacket(data)
		self.request.sendall(res_packet.getEncodedPacket().encode())


	def handle(self):
		
		raw = recv_json(self.request)
		if not raw:
			return

		packet = Packet()
		packet.decodePacket(raw)

		cmd = packet.getCommand()
		if cmd == "put":
			self.handle_put(packet)
		elif cmd == "get":
			self.handle_get(packet)

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

	node_path = f"{nodes_dir}/{DATA_NODE}"
	os.makedirs(node_path, exist_ok=True)

	register("localhost", META_PORT, HOST, PORT)

    # Create the server
	with socketserver.TCPServer((HOST, PORT), DataNodeTCPHandler) as server:
		# Activate the server; this will keep running until you
		# interrupt the program with Ctrl-C
		server.node_path = node_path
		server.serve_forever()
