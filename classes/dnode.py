import json

class DataNode:
	def __init__(self, id, address, port):
		self.id = id
		self.address = address
		self.port = port
		self.blocks = []

	def getConn(self):
		return (self.address, self.port)

	def saveData(self, dirpath):
		with open(f"{dirpath}/{self.id}.json", "w") as file:
			json.dump(self.__dict__, file, indent=2)

	def loadData(self, dirpath):
		with open(f"{dirpath}/{self.id}.json", "r") as file:
			data = json.load(file)
			self.__dict__.update(data)
