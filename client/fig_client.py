from init import conf_parse, socket_init
from sock_ops import pull_sync, push_sync
from fs_ops import construct_tree, differences
from debug import debug_print

import time

def main():
	conf = conf_parse()
	sock = socket_init(conf)

	debug_print("Initialization successful")
	debug_print("Checking remote")

	pull_sync(sock, conf["project"])
	debug_print("Pull successfull")

	client_tree = construct_tree()
	while True:
		if differences(client_tree):
			debug_print("Different spotted, pushing")
			client_tree = construct_tree()

			push_sync(sock, conf["project"])

		if conf["auto"]:
			time.sleep(conf["auto"])
		else:
			input("Enter to sync")

if __name__ == "__main__":
	main()