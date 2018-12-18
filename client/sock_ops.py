from packets import fetch, push, pull, delete
from debug import debug_print
from fs_ops import differences

import socket
import os
import pathlib
import json
import shutil

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


def fetch_server_version(sock, project):
	sock.sendall(fetch(project))
	server_structure = loop_recv(sock)
	if server_structure["status"] == "ok":
		debug_print("Fetch successful")
	else:
		debug_print("Error: " + server_structure["status"])

	if server_structure["status"] != "ok":
		debug_print("Status: " + server_structure["status"])
	print(server_structure)
	return server_structure["files"]

def pull_sync(sock, project):
	server_tree = fetch_server_version(sock, project)

	diff = differences(server_tree)

	for path in diff:
		debug_print("Pulling " + path)
		sock.sendall(pull(path))
		reply = await_reply(sock, path)
		if reply["write"]:
			# Write new stuff
			if reply["folder"]:
				if not os.path.exists(path):
					os.mkdir(path)
			else:
				with open(path, "w") as f:
					f.write(reply["file"])
		else:
			# Delete stuff
			try:
				if os.path.isdir(path):
					shutil.rmtree(path)
				else:
					os.remove(path)
			except FileNotFoundError:
				pass

		debug_print(path + " done writing to disk")

	debug_print("All files downloaded")

def push_sync(sock, project):
	diff = differences(fetch_server_version(sock, project))
	print(diff)
	if diff:
		debug_print("Local has newer files, uploading")
		for path in diff:
			if os.path.exists(path):
				push_to_socket(sock, path)
				if os.path.isdir(path):
					for item in pathlib.Path(path).rglob("*"):
						push_to_socket(sock, os.path.join(path, item))
			else:
				# Seized existing locally, send delete.
				debug_print("Deleting " + path)
				sock.sendall(delete(path))
				await_reply(sock, path)

		debug_print("All files uploaded")

def push_to_socket(sock, path):
	debug_print("Pushing " + path)
	sock.sendall(push(path))
	await_reply(sock, path)

def await_reply(sock, path):
	reply = loop_recv(sock)
	if reply["status"] == "ok":
		debug_print(path + " done loading")
	else:
		debug_print("Error: " + reply["status"])
	return reply

