import json

class Packet:
	def __init__(self):
	    self.client_commands = ['ls', 'put', 'get', 'rm', 'dblks']
        self.data_node_commands = ['reg', 'res']
	    self.packet = {}

	def getEncodedPacket(self):
	    return json.dumps(self.packet)

	def decodePacket(self):
		self.packet = json.loads(packet)

	def getCommand(self):
		if self.packet.has_key['cmd']:
			return self.packet['cmd']
		return None

	def getAddr(self):
		if self.packet.has_key['addr']:
			return self.packet['addr']
		return None

	def getPort(self):
		if self.packet.has_key['port']:
			return self.packet['port']
		return None

	def getData(self):
		if self.packet.has_key['data']:
			return self.packet['data']
		return None

    def buildClientPacket(self, cmd, params)
        if cmd in self.client_commands:
            self.packet = {'cmd': cmd, 'params': params}

    def buildMDPacket(self, data)
        self.packet = {'data': data}

    def buildDNPacket(self, cmd, addr, port)
        if cmd in self.data_node_commands:
            self.packet = {'cmd': cmd, 'addr': addr, 'port': port}

