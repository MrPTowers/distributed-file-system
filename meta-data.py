import socketserver
import sys

from classes.inode import iNode
from classes.packet import Packet

superblock = {"block_size": 4096, "inode_table": []}

def usage():
	print(f"Usage: python3 meta-data.py <port, default=8000>")
	sys.exit(0)	

class MetaTCPHandler(socketserver.BaseRequestHandler):

	def handle_reg(self, packet):
		print("reg handle") #TODO

	def handle_ls(self, packet):
		
		try:
			#TODO
			print("ls handle")
	
		except:
			self.request.sendall("NAK")

	def handle_put(self, packet):
		print("put handle") #TODO

	def handle_get(self, packet):
		print("get handle") #TODO

	def handle_rm(self, packet):
		print("rm handle")	#TODO

	def handle_blocks(self, packet):
		print("block handle") #TODO

	def handle(self):	
		packet = Packet()

		msg = self.request.recv(1024)	

		p.decodePacket(msg)

		#TODO
		

		if packet.cmd == "reg":
			self.handle_reg(packet)
		elif cmd == "ls":
			self.handle_ls(packet)
		elif cmd == "put":
			self.handle_put(packet)
		elif cmd == "get":
			self.handle_get(packet)
		elif cmd == "rm":
			self.handle_rm(packet)
		elif cmd == "dblks":
			self.handle_blocks(packet)
		else:
			print ("no command")

		print("Done with handle")

if __name__ == '__main__':
	HOST, PORT = "", 8000    

	#Check to see if program is run with the correct amount of arguments
	if len(sys.argv) > 1:
		try:
			PORT = int(sys.argv[1])
		except:
			usage()
	
	#TODO
	#Check if metadata jsons exist
		#If they do
			#Load existing iNode jsons into superblock
		#If they dont
			#Create the metadata jsons and add a single inode for the root directory

	# Create the server, binding to localhost on port 8000
	with socketserver.TCPServer((HOST, PORT), MetaTCPHandler) as server:
		# Activate the server; this will keep running until you
		# interrupt the program with Ctrl-C
		print(f"Metadata server running on localhost on port:{PORT}")
		server.serve_forever() 
