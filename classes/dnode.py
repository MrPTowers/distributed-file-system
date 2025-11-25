class DataNode:
	def __init__(self, id, address, port):
		self.id = id
		self.address = address
		self.port = port

	def getConn(self):
		return self.address, self.port
