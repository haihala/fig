import json
import os

def fetch():
	return bytes(json.dumps({
		"type": "fetch",
		"arguments": {}
	}))

def pull(path):
	return bytes(json.dumps({
		"type": "fetch",
		"arguments": {
			"path": path
		}
	}))

def push(path):
	isfile = os.path.isfile(path)
	if isfile:
		with open(path, "rb") as f:
			content = f.read()

	return bytes(json.dumps({
		"type": "fetch",
		"arguments": {
			"path": path,
			"isfile": isfile,
			"content": content
		}
	}))

def delete(path):
	return bytes(json.dumps({
		"type": "delete",
		"arguments": {
			"path": path
		}
	}))
