from debug import debug_print
from bfc import loop_recv
from packets import fetch_response, pull_response, push_response, delete_response

import socket
import socketserver
import os
import shutil

PROJECTS_FOLDER="."

class Fig_server(socketserver.BaseRequestHandler):
	def setup(self):
		self.current_projects = {}
		return super(Fig_server, self).setup()

	def handle(self):
		self.data = loop_recv(self.request)
		debug_print("{} wrote:".format(self.client_address[0]))
		debug_print(self.data)
		self.request.sendall(self.server_response())
		self.handle()

	def server_response(self):
		if self.data["type"] == "fetch":
			# Client requested the structure of a project
			self.current_projects[self.client_address] = os.path.join(PROJECTS_FOLDER, self.data["project"])
			sh = self.current_projects[self.client_address]		# ShortHand
			if not os.path.exists(sh):
				# New project
				os.mkdir(sh)
			return fetch_response(sh)

		elif self.data["type"] == "pull":
			# Client requested the contents of a file
			path_to_file=os.path.join(self.current_projects[self.client_address], self.data["path"])
			exists = os.path.exists(path_to_file)
			folder = os.path.isdir(path_to_file)
			contents = ""
			if exists and not folder:
				with open(path_to_file, 'r') as f:
					contents = f.read()
			return pull_response(contents, exists, folder)

		elif self.data["type"] == "push":
			# Client uploaded a file
			path_to_file=os.path.join(self.current_projects[self.client_address], self.data["path"])
			if self.data["isfile"]:
				with open(path_to_file, "w") as f:
					f.write(self.data["content"])
			else:
				os.mkdir(path_to_file)
			return push_response()

		elif self.data["type"] == "delete":
			# Client deleted a file
			path_to_file=os.path.join(self.current_projects[self.client_address], self.data["path"])
			if os.path.exists(path_to_file):
				if os.path.isdir(path_to_file):
					shutil.rmtree(path_to_file)
				else:
					os.remove(path_to_file)
				return delete_response()
			else:
				return delete_response(status="404")

if __name__ == "__main__":
	HOST, PORT = "localhost", 6969
	server = socketserver.TCPServer((HOST, PORT), Fig_server)
	server.serve_forever()