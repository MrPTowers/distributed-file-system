import json

class Packet:
	def __init__(self):
		self.client_commands = ['ls', 'put', 'get', 'rm', 'dblks']
		self.data_node_commands = ['reg', 'res']
		self.packet = {}

	def getEncodedPacket(self):
	    return json.dumps(self.packet)

	def decodePacket(self, packet):
		self.packet = json.loads(packet)

	def getCommand(self):
		if 'cmd' in self.packet:
			return self.packet['cmd']
		return None

	def getAddr(self):
		if 'addr' in self.packet:
			return self.packet['addr']
		return None

	def getPort(self):
		if 'port' in self.packet:			
			return self.packet['port']
		return None

	def getData(self):
		if 'data' in self.packet:			
			return self.packet['data']
		return None

	def buildClientPacket(self, cmd, params):
		if cmd in self.client_commands:
			self.packet = {'cmd': cmd, 'params': params}

	def buildMDPacket(self, data):
		self.packet = {'data': data}

	def buildDNPacket(self, cmd, addr, port):
		if cmd in self.data_node_commands:
			self.packet = {'cmd': cmd, 'addr': addr, 'port': port}

