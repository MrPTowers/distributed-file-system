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
		return json.dumps(self.packet)

	def decodePacket(self):
		self.packet = json.loads(packet)

	def getCommand(self):
		if self.packet.has_key["cmd"]:
			return self.packet["cmd"]
		return None

	def getAddr(self):
		if self.packet.has_key["addr"]:
			return self.packet["addr"]
		return None

	def getPort(self):
		if self.packet.has_key["port"]:
			return self.packet["port"]
		return None

	def getData(self):
		if self.packet.has_key["data"]:
			return self.packet["data"]
		return None

	def buildClientSendPacket(self, cmd, addr, port, data): #From cp and ls clients to meta-data server
		if cmd in self.commands:
			self.packet = {"cmd": cmd, "addr": addr, "port": port, "data": [data]}
			return True
		return False

	def buildClientReceivePacket(self, data): #From meta-data server to cp and ls clients
		self.packet = {"data": [data]}

	def buildDataSendPacket(self, cmd, data_ip, data_port):
		self.packet = {"cmd": cmd, "addr": data_ip, "port": data_port}

	def buildDataReceivePacket(self, meta_ip, meta_port, data):
		self.packet = {"addr": meta_ip, "port": meta_port, "data":[data]}

