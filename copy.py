import socket
import sys
import os
import json

from classes.packet import Packet
from classes.dnode import DataNode

block_size = 4096

def usage():
	print("Usage: python3 copy.py <server>:<port>:<dfs file path> <destination file>\nor\npython3 copy.py <source file> <server>:<port>:<dfs file path>")
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

def copyToDFS(address, file_name, path):

#Step 1: Metadata server (Send file info and receive data node list with conn)
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect(address)
		
		file_size = os.path.getsize(path)
		packet = Packet()
		if os.path.isdir(file_name): #If the file is a directory, append a list of files in the packet #Future feature
			#file_list = os.listdir(file_name)
			#packet.buildPacket("put", [path, file_size, file_list])
			#s.sendall(packet.getEncodedPacket().encode())
			print("Directories not yet implemented")
			s.close()
			return
		else: #If it is a single file, handle normally
			packet.buildPacket("put", [path, file_size])
			packet.packet["path"] = file_name
			s.sendall(packet.getEncodedPacket().encode())
		
		raw = recv_json(s)
		if not raw:
			print("Metadata server did not respond.")
			return

		rec_packet = Packet()
		rec_packet.decodePacket(raw)

	data = rec_packet.getData()	
	inode_id = data["inode_id"]
	data_nodes = data["data_nodes"]


#Step 2: Split file into chunks and send to available data nodes to store
	data_blocks = []
	i = 0
	with open(path, 'rb') as file:
		while True:
			chunk = file.read(block_size)
			if not chunk:
				break #File is done
			
			dn_address = data_nodes[i % len(data_nodes)]
			i += 1
			
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as dn_socket:
				dn_socket.connect(tuple(dn_address))
				
				data_packet = Packet()
				data_packet.buildPacket("put", chunk)
				dn_socket.sendall(data_packet.getEncodedPacket().encode())	
				
				raw = recv_json(dn_socket)
				if not raw:	
					print("Data node did not respond.")
					return

				res_packet = Packet()
				res_packet.decodePacket(raw)

				data_blocks.append((res_packet.getData(), dn_address))

#Step 3: Send uuids to metadata server with corresponding data node

	final_packet = Packet()
	final_packet.buildPacket("dblks", {
		"inode_id": inode_id,
		"blocks": data_blocks
    })

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as md_socket:
		md_socket.connect(address)
		md_socket.sendall(final_packet.getEncodedPacket().encode())

		raw = recv_json(md_socket)
		if raw:
			ack = Packet()
			ack.decodePacket(raw)
	print("Upload complete")

def copyFromDFS(address, file_name, path):
	
# Step 1: Ask metadata server for block list
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect(address)

		req_packet = Packet()
		req_packet.buildPacket("get", file_name)
		req_packet.packet["path"] = file_name
		s.sendall(req_packet.getEncodedPacket().encode())

		raw = recv_json(s)
		if not raw:
			print("Metadata server did not respond.")
			return

		res_packet = Packet()
		res_packet.decodePacket(raw)

	data = res_packet.getData()
	if data is None:
		print("File not found in DFS.")
		return

	inode_id = data["inode_id"]
	block_list = data["blocks"]
	data_nodes = data["data_nodes"]


# Step 2: Retrieve each block from the appropriate data node
	with open(path, "wb") as out:
		for i, (block_id, dn_addr) in enumerate(block_list):

			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as dn:
				dn.connect(tuple(dn_addr))

				get_packet = Packet()
				get_packet.buildPacket("get", block_id)
				dn.sendall(get_packet.getEncodedPacket().encode())

				raw = recv_json(dn)
				if not raw:
					print(f"Data node {dn_addr} failed to return block {block_id}")
					return

				res_packet = Packet()
				res_packet.decodePacket(raw)

				block_data = res_packet.getData()
				if block_data is None:
					print(f"Missing block {block_id}")
					return

				out.write(block_data)

	print("Download complete.")


if __name__ == "__main__":
	if len(sys.argv) < 3:
		usage()

	file_from = sys.argv[1].split(":")
	file_to = sys.argv[2].split(":")

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

		if os.path.exists(from_path):
			copyToDFS((ip, port), to_path, from_path)
		else:
			print("File does not exist")
