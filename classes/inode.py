class iNode:
	def __init__(self, id, file_type):
		self.id = id #inode id
		self.file_type = file_type #type of file. THis implementation only uses f or d for file or directory
		self.file_size = 0 #size of file in blocks
		self.direct_count = 12 #max pointers in first layer of inode
		self.ptr_per_block = 512 #amount of pointers allowed in any given data block starting with single indirect
		self.direct_blocks = [] #direct data block
		self.single_indirect = [] #single indirect block. points to data blocks
		self.double_indirect = [] #double indirect block. points to single indirect blocks
		self.triple_indirect = [] #triple indirect block points to double indirect blocks
		
		self.levels = [
			(self.direct_count, self.dblocks),
			(self.ptr_per_block, self.sind),
			(self.ptr_per_block, self.dind),
			(self.ptr_per_block, self.tind),
		]

	def insert_block_recursive(self, level, max_width, block, bid):
        
        #Base Case: There is space in the block
		if level == 0:
			if len(block) < max_width:
				block.append(bid)
				self.file_size = self.file_size + 1
				return True
			return False

        #Recursive Step: 
        
        # (a) Traverse deeper into indirects
		for sub_block in block:
			if self.insert_block_recursive(level - 1, max_width, sub_block, bid):
				return True

        # (b) All existing blocks are full. Create new block
		if len(block) < max_width:
			new_block = []
			block.append(new_block)
			return self.insert_block_recursive(level - 1, max_width, new_block, bid)

        #Worst Case: Everything is full
		return False

	def insertBlock(self, bid):
		for level, (max_width, block) in enumerate(self.levels):
			if self.insert_block_recursive(level, max_width, block, bid):
				print("Block inserted")
			else:
				print("File is too big. Chill out.")

	def get_block_ids_recursive(self, level, block):
        #Base Case: Direct data blocks
		if level == 0:
			return block[:]
        
		all_block_ids = []
		#Recursive Step: Find blocks of all levels below current
		for sub_block in block:
			all_ids.extend(self.get_block_ids_recursive(level - 1, sub_block))

		return all_ids

	def getBlocksIds(self):
		all_block_ids = []
		for level, (_, block) in enumerate(self.levels):
			all_blocks_ids.extend(self.get_block_ids_recursive(level, block))
		return all_blocks_ids
       
	def getSize(self):
		return self.fsize

	def getType(self):
		return self.ftype

