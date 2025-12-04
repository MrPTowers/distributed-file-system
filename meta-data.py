import socketserver
import sys
import os
import json

from classes.inode import iNode
from classes.dnode import DataNode
from classes.packet import Packet

superblock = [] #Array to store all inode metadata
data_nodes = [] #Array to store all data node metadata

inodes_filepath = "dfs_data/metadata/inodes" #Filepath variables for creating and loading files
data_nodes_filepath = "dfs_data/metadata/data_nodes" 

def usage():
	print(f"Usage: python3 meta-data.py <port, default=8000>")
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

class MetaTCPHandler(socketserver.BaseRequestHandler):

	def handle_reg(self, packet):
	   #Handle data node registration
		reg_addr = packet.getAddr()
		reg_port = packet.getPort()

		if len(data_nodes) == 0: #If first data node, simply register
			dnode = DataNode("0", reg_addr, reg_port)
			dnode.saveData(data_nodes_filepath)
			data_nodes.append(dnode) #Append data node to data nodes array
			msg = "ACK"
		else:
			for data_node in data_nodes:
				dnode_addr, dnode_port = data_node.getConn()
				if dnode_addr == reg_addr and dnode_port == reg_port: #If addr and port match, node is already registered
					msg = "DUP"
					self.request.sendall(msg.encode())
					print("Duplicate data node")
					return
			reg_id = len(data_nodes)
			dnode = DataNode(reg_id, reg_addr, reg_port)
			dnode.saveData(data_nodes_filepath)
			data_nodes.append(dnode) #Append data node to data nodes array
			msg = "ACK"
		self.request.sendall(msg.encode())
		print("Data node registration request processed")

	def handle_ls(self):
	   #Handle ls request from ls client 
		try:
			# Start with root
			msg = "/\n"

			root = superblock[0]
			entries = root.getEntries()
			if entries:
				for name, inode_id in entries:
					msg += f"{name}\n"

			# Also list entries from other directories
			for inode in superblock[1:]:
				if inode.file_type == "d":
					dir_entries = inode.getEntries()
					if dir_entries:
						for name, inode_id in dir_entries:
							msg += f"{name}\n"

			self.request.sendall(msg.encode())

		except Exception as e:
			print("Error in handle_ls:", e)
			self.request.sendall(b"NAK")

		print("ls request processed")

	def handle_put(self, packet):
		#Handle put request (from copy client)
		send_packet = Packet()
		try:
			data = packet.getData()

			# Directory upload not implemented yet
			if isinstance(data, list) and len(data) == 3:
				print("directory not yet implemented")
				return

			raw_path = packet.getPath()
			if raw_path:
				dfs_name = raw_path.split(":")[-1]
			else:
				dfs_name = data[0]

			# Create inode
			inode_id = len(superblock)
			inode = iNode(inode_id, 'f')
			superblock.append(inode)
			superblock.sort(key=lambda inode: int(inode.id))
			inode.saveData(inodes_filepath)

			# Insert into root directory
			root = superblock[0]
			root.insertEntry(dfs_name, inode_id)
			root.saveData(inodes_filepath)
			
			# Prepare list of data nodes to return
			dn_list = [dn.getConn() for dn in data_nodes]

			send_packet.buildMDPacket({
				"inode_id": inode_id,
				"data_nodes": dn_list
			})

		except Exception as e:
			print("[MD] Error in handle_put:", e)
			send_packet.buildMDPacket("NAK")

		self.request.sendall(send_packet.getEncodedPacket().encode())
		print("put request processed")
	
	def handle_get(self, packet):
		#Handle get request (from copy) 		
		try:
			path = packet.getPath()
			if path is None:
				path = packet.getData()

			print(f"[MD] GET lookup for name: {path}")

			root = superblock[0]
			entries = root.getEntries()

			target_inode = None

			if entries:
				for name, inode_id in entries:
					if name == path:
						target_inode = superblock[int(inode_id)]
						break

			if target_inode is None:
				resp = Packet()
				resp.buildMDPacket(None)
				self.request.sendall(resp.getEncodedPacket().encode())
				print(f"[MD] File '{path}' not found.")
				return

			block_ids = target_inode.getBlocksIds()

			# Reconstruct which datanode holds each block (round robin)
			block_list = []
			for i, bid in enumerate(block_ids):
				dn = data_nodes[i % len(data_nodes)]
				block_list.append((bid, dn.getConn()))

			resp = Packet()
			resp.buildMDPacket({
				"inode_id": target_inode.id,
				"blocks": block_list,
				"data_nodes": [dn.getConn() for dn in data_nodes]
			})

			self.request.sendall(resp.getEncodedPacket().encode())
			print(f"[MD] GET request → sent block list for inode {target_inode.id}")

		except Exception as e:
			print("[MD] Error in handle_get:", e)
			resp = Packet()
			resp.buildMDPacket(None)
			self.request.sendall(resp.getEncodedPacket().encode())


	def handle_blocks(self, packet):

		try:
			data = packet.getData()

			inode_id = int(data["inode_id"])
			blocks = data["blocks"]

			inode = superblock[inode_id]

			# Insert block UUIDs in order
			for block_uuid, dn_info in blocks:
				inode.insertBlock(block_uuid)

			# Save updated inode file
			inode.saveData(inodes_filepath)

			print(f"[MD] handle_blocks → inode {inode_id} updated with {len(blocks)} blocks")

			# Respond to client
			res_packet = Packet()
			res_packet.buildMDPacket("ACK")
			self.request.sendall(res_packet.getEncodedPacket().encode())

		except Exception as e:
			print("[MD] Error in handle_blocks:", e)
			res_packet = Packet()
			res_packet.buildMDPacket("NAK")
			self.request.sendall(res_packet.getEncodedPacket().encode())


	def handle(self):
		packet = Packet()

		raw = recv_json(self.request)
		if not raw:
			return
		packet.decodePacket(raw)		
		
		print(f"Received {packet.getCommand()} request")
		cmd = packet.getCommand()

		if cmd == "reg":
			self.handle_reg(packet)
		elif cmd == "ls":
			self.handle_ls()
		elif cmd == "put":
			self.handle_put(packet)
		elif cmd == "get":
			self.handle_get(packet)
		elif cmd == "dblks":
			self.handle_blocks(packet)
		else:
			print ("No command received")

		print("Message fully handled")

if __name__ == '__main__':
	HOST, PORT = "", 8000    

	#Check to see if program is run with the correct amount of arguments
	if len(sys.argv) > 1:
		try:
			PORT = int(sys.argv[1])
		except:
			usage()
	
	os.makedirs(inodes_filepath, exist_ok=True) #Make the main dfs, metadata, and inodes folders if they don't exist already.
	if not os.path.exists(f"{inodes_filepath}/0.json"): #If no root directory json exists, make it
		root = iNode(0, "d")
		superblock.append(root) #Insert iNode object into the superblock
		root.saveData(inodes_filepath) #Save root directory json
	else: #If root directory json exists, load all existing inode metadata into superblock
		for filename in os.listdir(inodes_filepath):
			inode_id = filename.split(".")[0] #Files are named as #.json where # is the inode id number
			inode = iNode(inode_id, "")
			inode.loadData(inodes_filepath) #Restore relevant metadata to inode object
			superblock.append(inode) #Append inode object to superblock
		superblock.sort(key=lambda inode: int(inode.id)) #Sort all inodes in order of id

	if not os.path.isdir(data_nodes_filepath): #Repeat inode process for data nodes
		os.mkdir(data_nodes_filepath)
	else:
		for filename in os.listdir(data_nodes_filepath):
			data_node_id = filename.split(".")[0]
			dnode = DataNode(data_node_id, "", 0)
			dnode.loadData(data_nodes_filepath)
			data_nodes.append(dnode)
		data_nodes.sort(key=lambda dnode: int(dnode.id))

	# Create the server, binding to localhost on port 8000
	with socketserver.TCPServer((HOST, PORT), MetaTCPHandler) as server:
		# Activate the server; this will keep running until you
		# interrupt the program with Ctrl-C
		print(f"Metadata server running on localhost on port:{PORT}")
		server.serve_forever() 
