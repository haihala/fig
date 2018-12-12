import os
import json
import socket


DEFAULT_CONF = {
	"auto": 5,
	"port": 6969
}

def conf_parse():
	conf = DEFAULT_CONF

	assert os.path.isfile("fig_conf.json"), ("Configuration file 'fig_conf.json' not detected in current working directory.")

	with open("fig_conf.json", "r") as f:
		conf.update(json.loads(f.read()))

	assert ("server" in conf), ("Configuration file does not specify server.")
	assert ("project" in conf), ("Configuration file does not specify project.")

	return conf

def socket_init(conf):
	server = conf["server"]
	port = conf["port"]

	sock = socket.create_connection((server, port))

	return sock