import json

class Packet:
	def __init__(self):
		#Commands:
		#Register a data node
		#List all files in dfs
		#Put a file in dfs
		#Get a file from dfs
		#Remove a file from dfs
		#Add data block ids to file
		self.commands = ['reg', 'ls', 'put', 'get', 'rm', 'dblks']
		self.packet = {}

	def getEncodedPacket(self):
		print(" ")		

	def decodePacket(self):
		print(" ")

	def getCommand(self):
		print(" ")

	def getAddr(self):
		print(" ")

	def getPort(self):
		print(" ")

	def getData(self):
		print(" ")

	def buildSendPacket(self, cmd, addr, port):
		self.packet = {"cmd": cmd, "addr": addr, "port": port, "data": []}

	def buildReceivePacket(self, ):
		print(" ")

