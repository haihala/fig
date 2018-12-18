import hashlib
import os
import json
import pathlib

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
	if "fig_conf.json" in tree:
		del tree["fig_conf.json"]
	return tree

def differences(main_tree):
	print(main_tree)
	"""
	Returns the paths of all files that have different md5sums and folders that don't exist in both versions.
	"""
	local_tree = construct_tree()
	print(local_tree)
	diff = recursive_diffs(main_tree, local_tree).union(recursive_diffs(local_tree, main_tree))

	return diff

def recursive_diffs(main_tree, secondary_tree, root=''):
	diff = set()

	for item in main_tree:
		path = os.path.join(root, item)
		if type(main_tree[item]) == type({}):
			if item not in secondary_tree:
				diff.add(path)
				diff = diff.union(set(str(i) for i in pathlib.Path(path).rglob("*")))
			else:
				diff = diff.union(recursive_diffs(main_tree[item], secondary_tree[item], path))
		elif item not in secondary_tree or main_tree[item] != secondary_tree[item]:
			diff.add(path)

	return diff

if __name__ == '__main__':
	print(differences({"fold": {"fold": {"test": ""}}, "test.txt": "aoeu"}))