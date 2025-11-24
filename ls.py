import socket

def usage():
	print("Usage: python3 ls.py <server>:<port, default=8000>")
	sys.exit(0)

def client(ip, port):
	return 0


if __name__ == "__main__":
	if len(sys.argv) < 2:
		usage()

	ip = None
	port = 8000 
	server = sys.argv[1].split(":")
	if len(server == 1):
		ip = server[0]
	elif len(server == 2):
		ip = server[0]
		port = int server[1]

	if not ip:
		usage()

	client(ip, port)
