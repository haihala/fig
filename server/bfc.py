# Burrowed from client
import json
import socket
import os
import hashlib

SIZE = 1024

def loop_recv(sock):
	chunk = sock.recv(SIZE)
	result = chunk
	while len(chunk) == SIZE:	# If chunk is exactly size, there can be more to come.
		chunk = sock.recv(SIZE)
		result += chunk
	response=result.decode("UTF-8")
	if response:
		return json.loads(response)


def md5sum(path):
	hasher = hashlib.md5()
	with open(path, 'rb') as f:
		content = f.read()
	hasher.update(content)
	return hasher.hexdigest()

def construct_tree(root='.'):
	tree = {}

	for item in os.listdir(root):
		path = os.path.join(root, item)
		if os.path.isfile(path):
			tree[item] = md5sum(path)
		else:
			tree[item] = construct_tree(root=path)

	return tree
