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

	def decodePacket(self):
