import socketserver
import sys
import os
import json

from classes.inode import iNode
from classes.dnode import DataNode
from classes.packet import Packet

superblock = {"block_size": 4096, "inode_table": []} #Dict to store all inode metadata
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
			print("Here")
			dnode = DataNode("0", reg_addr, reg_port)
			dnode.saveData(data_nodes_filepath)
			data_nodes.append(dnode) #Append data node to data nodes array
			msg = "ACK"
		else:
			print("here instead")
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
		print(msg)
		self.request.sendall(msg.encode())
		print("Data node register request processed")

	def handle_ls(self):
        #Handle ls request from ls client 
		try:
			msg = ""
			inode_table = superblock["inode_table"]
			for i in range(len(inode_table)):
				if i == 0: #First inode will always be root
					msg = "/\n"
					entries = inode_table[i].getEntries()
					for entry in entries:
						msg = msg + f"/{entry[0]}\n"
				else:
					if inode_table[i].file_type == "d":
						entries = inode_table[i].getEntries()
						for entry in entries:
							msg = msg + f"/{entry[0]}\n"
			self.request.sendall(msg.encode())

		except:
			self.request.sendall("NAK")

		print("Ls request processed")

	def handle_put(self, packet):
		print("put handle") #TODO

	def handle_get(self, packet):
		print("get handle") #TODO

	def handle_rm(self, packet):
		#Handle rm request from rm client
		print("rm handle")	#TODO

	def handle_blocks(self, packet):
		print("block handle") #TODO

	def handle(self):
		packet = Packet()

		msg = self.request.recv(1024)	
		
		packet.decodePacket(msg)
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
		elif cmd == "rm":
			self.handle_rm(packet)
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
			superblock["inode_table"].append(root) #Insert iNode object into the superblock
			root.saveData(inodes_filepath) #Save root directory json
		else: #If root directory json exists, load all existing inode metadata into superblock
			for filename in os.listdir(inodes_filepath):
				inode_id = filename.split(".")[0] #Files are named as #.json where # is the inode id number
				inode = iNode(inode_id, "")
				inode.loadData(inodes_filepath) #Restore relevant metadata to inode object
				superblock["inode_table"].append(inode) #Append inode object to superblock
			superblock["inode_table"].sort(key=lambda inode: inode.id) #Sort all inodes in order of id

		if not os.path.isdir(data_nodes_filepath): #Repeat inode process for data nodes
			os.mkdir(data_nodes_filepath)
		else:
			for filename in os.listdir(data_nodes_filepath):
				data_node_id = filename.split(".")[0]
				dnode = DataNode(data_node_id, "", 0)
				dnode.loadData(data_nodes_filepath)
				data_nodes.append(dnode)
			data_nodes.sort(key=lambda dnode: dnode.id)

		#if not os.path.exists(dn_filepath): #If data node file doesn't exist, make it.
		#	with open(dn_filepath, "w") as dn_file:
		#		pass #File will be empty until data node is registered
		#else:
		#	with open(dn_filepath, "r") as dn_file: #If it exists, load its data
		#		dn_data = json.load(dn_file)
		#		for dnode in len(dn_data): #Store existing dnode metadata in data_block dict
		#			print("dnode")


	# Create the server, binding to localhost on port 8000
	with socketserver.TCPServer((HOST, PORT), MetaTCPHandler) as server:
		# Activate the server; this will keep running until you
		# interrupt the program with Ctrl-C
		print(f"Metadata server running on localhost on port:{PORT}")
		server.serve_forever() 
