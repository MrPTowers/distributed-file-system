import socket
import sys
import os

def usage():
	print("Usage: python3 copy.py <server>:<port>:<dfs file path> <destination file>")
	sys.exit(0)

def copyToDFS(address, fname, path):


def copyFromDFS(address, fname, path):


if __name__ == "__main__":
	if len(sys.argv) < 3:
		usage()

	file_from = sys.argv[1].split(":")
	file_to = sys.argv[2].split(":")

	if (len(file_from) > 1):
		ip = file_from[0]
		port = int(file_from[1])
		from_path = file_from[2]
		to_path = sys.argv[2]

		copyFromDFS((ip, port), from_path, to_path)

	elif len(file_to) > 2:
		ip = file_to[0]
		port = int(file_to[1])
		to_path = file_to[2]
		from_path = sys.argv[1]

		copyToDFS((ip, port), to_path, from_path)
