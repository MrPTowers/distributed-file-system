# distributed-file-system
 Pablo Torres Arroyo  
 801-19-7744  
 03/12/2025  

### Libraries used:
---

Socket / SocketServer — TCP communication
JSON — packet transport formatting
Base64 — safe binary transfer
UUID — generating block IDs
OS — file paths, directory creation
Sys — argument parsing


### How to run
---

The project consists of 4 separate programs and 3 custom libraries:

Custom libraries:

1. iNode: Stores all important metadata for a file
2. DataNode: Stores information on data note addresses
3. Packet: Manages packet structure and functionality

Programs:

- meta-data.py

Use: python3 meta-data.py <port, default=8000>

The program acts as a server that waits for messages from clients or data nodes. It handles ls, put, get, blks, and reg requests.

- data-node.py

Use: python3 data-node.py <server address> <port> <data path> <metadata port, default=8000>

The program acts as a data storage disk. It sends a reg request to the meta-data server and waits for client requests. It handles put and get requests.

- ls.py

Use: python3 ls.py <server>:<port, default=8000>

The program sends a single request to the meta-data server in order to get a list of all files in the dfs

- copy.py

Uses: 
python3 copy.py <server>:<port>:<dfs file path> <destination file>
python3 copy.py <source file> <server>:<port>:<dfs file path>

The program can copy a file into or out of the dfs. It connects to the metadata server and each data-node in order to extract the necessary info to decompose the file into data blocks or recompose it from them.

Request types:
- ls: Request to list all files in the dfs
- put: Request to insert a new file into the dfs (to md server) or to write a new file block (to data node)
- get: Request to get block uuids from inode (from md server) or request to receive data block (from data node)
- blks: Request to insert data blocks uuids into inode
- reg: Request to register a data node


### Sources consulted
---

Online:
1. https://www.geeksforgeeks.org/operating-systems/inode-in-operating-system/
UNIX implementation of inodes
2. https://docs.python.org/3/library/socketserver.html
Initial socket server templates

People:
1. Uriel Fuentes: Discussed chunk splitting methods and challenges
2. Gabriel Romero: Discussed complex iNode structure


### Pontential Improvements
---
- Implement directories
- Implement cryptography on file blocks
- Remove possibility for same named files
