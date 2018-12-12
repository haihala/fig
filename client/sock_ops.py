from packets import fetch, push, pull, delete
from debug import debug_print
from fs_ops import differences

import socket
import os
import pathlib
import json

SIZE = 1024

def loop_recv(sock):
	result = ""
	while result % SIZE == 0 or result.endswith('\n'):
		result += sock.recv(SIZE)

	return json.loads(result.encode("UTF-8"))

def fetch_server_version(sock):
	sock.send(fetch())
	server_structure = loop_recv(sock)
	if server_structure["status"] == "ok":
		debug_print("Fetch successful")
	else:
		debug_print("Error: " + server_structure["status"])
	return server_structure["files"], server_structure["times"]

def pull_sync(sock):
	server_tree, server_times = fetch_server_version(sock)

	diff = differences(server_tree, server_times)
	if diff:
		debug_print("Remote has newer files, downloading")

	for path in diff:
		debug_print("Pulling " + path)
		sock.send(pull(path))
		reply = await_reply(sock, path)
		with open(path, "wb") as f:
			f.write(reply["file"])
		debug_print(path + " done writing to disk")

	debug_print("All files downloaded")

def push_sync(sock):
	diff = differences(*fetch_server_version(sock))
	if diff:
		debug_print("Local has newer files, uploading")
		for path in diff:
			if os.path.exists(path):
				if os.path.isfile(path):
					push_to_socket(sock, path)
				else:
					for item in pathlib.Path(path).rglob("*"):
						push_to_socket(sock, os.path.join(path, item))
			else:
				# Seized existing locally, send delete.
				debug_print("Deleting " + path)
				sock.send(delete(path))
				await_reply(sock, path)

		debug_print("All files uploaded")

def push_to_socket(sock, path):
	debug_print("Pushing " + path)
	sock.send(push(path))
	await_reply(sock, path)

def await_reply(sock, path):
	reply = loop_recv(sock)
	if reply["status"] == "ok":
		debug_print(path + " done loading")
	else:
		debug_print("Error: " + reply["status"])
	return reply

