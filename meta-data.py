import socketserver
import time
import sys

superblock = {}

def usage():
	print(f"Usage: python3 <server_address>  <port, default=8000>")
	sys.exit(0)	

class MetaTCPHandler(socketserver.BaseRequestHandler):

	def handle_reg(self, db, packet):

	def handle_ls(self, db, packet):

	def handle_put(self, db, packet):

	def handle_get(self, db, packet):

	def handle_blocks(self, db, packet):

	def handle(self):


def  main():
	


##main END


if __name__ == '__main__':
	HOST, PORT = "localhost", 8000    

	#Check to see if program is run with the correct amount of arguments
	if len(sys.argv) > 1:
		try:
			port = int(sys.argv[1])  
		except:
			usage()

    # Create the server, binding to localhost on port 8000
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
