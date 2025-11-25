class DataBlock():
	def __init__(self, block_id, data_node):
		self.id = block_id
		self.data_node = data_node

	def getInfo(self):
		return self.id, self.data_node
