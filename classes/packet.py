import json
import base64

class Packet:
	def __init__(self):
		self.client_commands = ["ls", "put", "get", "dblks"]
		self.data_node_commands = ["reg"]
		self.packet = {}

	def getEncodedPacket(self):
	    return json.dumps(self.packet)

	def decodePacket(self, packet):
		self.packet = json.loads(packet)

		data = self.packet.get("data")

		cmd = self.packet.get("cmd")

		if cmd == "put" and isinstance(data, str):
			try:
				self.packet["data"] = base64.b64decode(data)
				return
			except:
				return

		if isinstance(data, str) and (data.endswith("=") or data.endswith("==")):
			try:
				self.packet["data"] = base64.b64decode(data)
				return
			except:
				pass

		return

	def getCommand(self):
		if "cmd" in self.packet:
			return self.packet["cmd"]
		return None

	def getAddr(self):
		if "addr" in self.packet:
			return self.packet["addr"]
		return None

	def getPort(self):
		if "port" in self.packet:			
			return self.packet["port"]
		return None

	def getData(self):
		if "data" in self.packet:
			return self.packet["data"]
		return None

	def getPath(self):
		if "path" in self.packet:
			return self.packet["path"]
		return None

	def buildPacket(self, cmd, data):
		if cmd in self.client_commands:
			if isinstance(data, bytes):
				data = base64.b64encode(data).decode()
			self.packet = {"cmd": cmd, "data": data}

	def buildMDPacket(self, data):
		# If data is raw bytes, base64 encode
		if isinstance(data, bytes):
			data = base64.b64encode(data).decode()

		# If data is a dict, encode any byte fields
		elif isinstance(data, dict):
			fixed = {}
			for key, val in data.items():
				if isinstance(val, bytes):
					fixed[key] = base64.b64encode(val).decode()
				else:
					fixed[key] = val
			data = fixed

		self.packet = {"data": data}

	def buildDNPacket(self, cmd, addr, port):
		if cmd in self.data_node_commands:
			self.packet = {"cmd": cmd, "addr": addr, "port": port}
