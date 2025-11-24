class iNode:
	def __init__(self, id, ftype):
		self.id = id #inode id
		self.ftype = ftype #type of file. THis implementation only uses f or d for file or directory
		self.fsize = 0 #size of file in blocks
		self.dblocks = [] #data block. Max size is 12
		self.sind = [] #single indirect block. points to data blocks
		self.dind = [] #double indirect block. points to single indirect blocks
		self.tind = [] #triple indirect block points to double indirect blocks

	def insertBlock(self, bid):


	def getBlocks(self):

	
	def getSize(self):
		return self.fsize

	def getType(self):
		return self.ftype
