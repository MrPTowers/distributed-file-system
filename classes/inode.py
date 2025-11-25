class iNode:
	def __init__(self, id, file_type):
		self.id = id #inode id
		self.file_type = ftype #type of file. THis implementation only uses f or d for file or directory
		self.file_size = 0 #size of file in blocks
        self.direct_count = 12 #max pointers in first layer of inode
        self.ptr_per_block = 512 #amount of pointers allowed in any given data block starting with single indirect
		self.dblocks = [] #direct data block
		self.sind = [] #single indirect block. points to data blocks
		self.dind = [] #double indirect block. points to single indirect blocks
		self.tind = [] #triple indirect block points to double indirect blocks

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
        for subblock in block:
            if self.insert_block_recursive(level - 1, max_width, subblock, bid):
                return True

        # (b) All existing blocks are full. Create new block
        if len(block) < max_width:
            new_block = []
            block.append(new_block)
            return self.insert_block_recursive(level - 1, max_width, new_block, bid)

        #Worst Case: Everything is full
        return False

	def insertBlock(self, bid):
        for depth, (max_width, block) in enumerate(self.levels):
            if self.insert_block_recursive(depth, max_width, block, bid):
                print("Block inserted")

        print("File is too big. Chill out.")

    def get_block_ids_recursive(self, depth, block):
        #Base Case: Direct data blocks
        if depth == 0:
            return block[:]
        
        all_block_ids = []
        for subblock in block:
            all_ids.extend(self.get_block_ids_recursive(depth - 1, subblock))

        return all_ids

	def getBlocksIds(self):
        all_block_ids = []
        for depth, (_, block) in enumerate(self.levels):
            all_blocks_ids.extend(self.get_block_ids_recursive(depth, block))
        return all_blocks_ids
        


	def getSize(self):
		return self.fsize

	def getType(self):
		return self.ftype
