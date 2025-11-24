import uuid
import socket
import socketserver
import time
import sys
import subprocess


def usage():
	print(f"Usage: python3 data-node.py <server address> <port> <data path> <metadata port,default=8000">
	sys.exit(0)

class DataNodeTCPHandler(socketserver.BaseRequestHandler):
	def handle_put(self, packet):

	def handle_get(self, packet):

	def handle(self):

def  main():




##main END


if __name__ == '__main__':
	META_PORT = 8000    

	#Check to see if program is run with the correct amount of arguments
	if len(sys.argv) < 4:
		usage()
	
	try:
		HOST = sys.argv[1]
		PORT = int(sys.argv[2])
		DATA_PATH = sys.argv[3]

		if len(sys.argv > 4):
			META_PORT = int(sys.argv[4])

		if not os.path.isdir(DATA_PATH):
			print(f"Error: Data path DATA_PATH{} is not a directory.")
			usage()
	except:
		usage()

    # Create the server, binding to localhost on port 8000
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
