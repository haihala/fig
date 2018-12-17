from bfc import construct_tree

import json

def fetch_response(project_path):
	tree, error = construct_tree(root=project_path)
	if error:
		status = error
	else:
		status = "ok"

	packet = {
		"files": tree,
		"status": status
	}
	return json.dumps(packet).encode("UTF-8")

def pull_response(file_contents, exists, folder, status="ok"):
	return json.dumps({
		"file": file_contents,
		"write": exists,
		"folder": folder,
		"status": status
	}).encode("UTF-8")

def push_response(status="ok"):
	return json.dumps({
		"status": status
	}).encode("UTF-8")


def delete_response(status="ok"):
	return json.dumps({
		"status": status
	}).encode("UTF-8")
