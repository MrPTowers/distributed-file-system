import sqlite3

conn = sqlite.connect('dfs.b')

c = conn.cursor()

#Data node table
c.execute('CREATE TABLE dnode(nid INTEGER PRIMARY KEY ASC AUTOINCREMENT, address TEXT NOT NULL default " ", port INTEGER NOT NULL DEFAULT "0")')

#unique tuple

#inode table

#ID, FTYPE, FSIZE, 12 PTRS, 1 INDIRECT START NULL, 2 INDIRECT START NULL, 3 INDIRECT START NULL

c.execute('CREATE TABLE inode (fid INTEGER PRIMARY KEY ASC AUTOINCREMENT, ftype TEXT NOT NULL default "file", fsize INTEGER NOT NULL default '0')')

#directory entry table
c.execute('CREATE TABLE dentry (did INTEGER PRIMARY KEY ASC AUTOINCREMENT)')

#data block table

#ID, NID, CID

c.execute('CREATE TABLE block (bid INTEGER PRIMARY KEY ASC AUTOINCREMENT)')

#unique tuple

