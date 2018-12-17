import json
import os

def fetch(project):
	return json.dumps({
		"type": "fetch",
		"project": project
	}).encode("UTF-8")

def pull(path):
	return json.dumps({
		"type": "pull",
		"path": path
	}).encode("UTF-8")

def push(path):
	isfile = os.path.isfile(path)
	content = ""
	if isfile:
		with open(path, "rb") as f:
			content = f.read().decode("UTF-8")

	return json.dumps({
		"type": "push",
		"path": path,
		"isfile": isfile,
		"content": content
	}).encode("UTF-8")

def delete(path):
	return json.dumps({
		"type": "delete",
		"path": path
	}).encode("UTF-8")
