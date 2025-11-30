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
			reg_id = len(data_nodes) - 1
			dnode = DataNode(reg_id, reg_addr, reg_port)
			dnode.saveData(data_nodes_filepath)
			data_nodes.append(dnode) #Append data node to data nodes array
			msg = "ACK"
		self.request.sendall(msg.encode())
		print("Data node register request processed")

	def handle_res(self, packet):
		#Handle data node response (for copy and rm)
		print("res handle")

	def handle_ls(self):
        #Handle ls request from ls client 
		try:
			msg = ""
			for i in range(len(superblock)):
				if i == 0: #First inode will always be root
					msg = "/\n"
					entries = superblock[i].getEntries()
					for entry in entries:
						msg = msg + f"{entry[0]}\n"
				else: #Might need to revisit later
					if superblock[i].file_type == "d":
						entries = superblock[i].getEntries()
						for entry in entries:
							msg = msg + f"{entry[0]}\n"
			self.request.sendall(msg.encode()) #Send complete ls message
		except:
			self.request.sendall("NAK")

		print("ls request processed")

	def handle_put(self, packet):
		#Handle put request (from copy client)
		send_packet = Packet()
		try:
			inode_id = len(superblock)
			data = packet.getData()
			if len(data) == 3: #Upload is a directory
				print("directory")						
			elif len(data) == 2: #Upload is a single file
				inode = Inode(inode_id, 'f') #Make new inode for file
				superblock.append(inode) #Append to superblock
				send_packet.buildMDPacket(data_nodes) #Prep packet to send back to copy with data node objects
				self.request.sendall(send_packet.getEncodedPacket().encode())
		except:
			print("error")

		print("put request processed") #TODO

	def handle_get(self, packet):
		#Handle get request (from copy client)

		print("get handle") #TODO


	def handle_blocks(self, packet):
		#Handle blocks request (from copy client)
		print("block handle") #TODO

	def handle(self):
		packet = Packet()

		msg = self.request.recv(1024)	
		
		packet.decodePacket(msg)
		print(f"Received {packet.getCommand()} request")
		cmd = packet.getCommand()

		if cmd == "reg":
			self.handle_reg(packet)
		elif cmd == "res":
			self.handle_res(packet)
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
		superblock.sort(key=lambda inode: inode.id) #Sort all inodes in order of id

	if not os.path.isdir(data_nodes_filepath): #Repeat inode process for data nodes
		os.mkdir(data_nodes_filepath)
	else:
		for filename in os.listdir(data_nodes_filepath):
			data_node_id = filename.split(".")[0]
			dnode = DataNode(data_node_id, "", 0)
			dnode.loadData(data_nodes_filepath)
			data_nodes.append(dnode)
		data_nodes.sort(key=lambda dnode: dnode.id)

	# Create the server, binding to localhost on port 8000
	with socketserver.TCPServer((HOST, PORT), MetaTCPHandler) as server:
		# Activate the server; this will keep running until you
		# interrupt the program with Ctrl-C
		print(f"Metadata server running on localhost on port:{PORT}")
		server.serve_forever() 
