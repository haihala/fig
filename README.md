# Fig

Folder sharing tool. Intended team size is one. When started, it will pull down the most recent version and after that it'll upload all changes.

## Installation

Just run either `fig_client.py` or `fig_server.py`. Adding them to your path is a good idea.

## Usage

Run this in a folder with a configuration file called `fig_conf.json`. Configuration file must exist and contain at least the mandatory options.

## Configuration

All configuration is placed in a file called `fig_conf.json`. Here is an example configuration file with default values for those that apply.

```json
{
	"server": "",		// Mandatory string ip of server you are connecting to.
	"port": 6969,		// Optional integer port on server.
	"project": "",		// Mandatory string project on server you are syncing to.
	"auto": 0			// Optional integer seconds between syncing to server. 0 disables automatic synchronization entirely.
}
```

## Comms

Client sends out packages and gets replies. Server never initiates. Here is a list of packages the client can send and the matching server responses with some explanations.

### Fetch

Arguments:

* name of project

Get a json object that describes the master structure and md5sums of the files and the unix timestamps they were pushed to server.

Example folder structure:

* foo
	* foo.png
* bar
	* bur
		* bur.py
	* bar.txt

Example returns:

```json
{
	"files": {
		"foo": {
			"foo.png": "<md5sum of foo.png>"
		},
		"bar": {
			"bur": {
				"bur.py": "<md5sum of bur.py>"
			},
			"bar.txt": "<md5sum of bar.txt>"
		}
	},
	"status": "ok"
}
```

### Pull

Arguments:

* path of file

Client indicates that their version of the named file is out of date and is requesting it from the server.

Returns:

* file - bytes contents of the file if is file. doesn't matter elsewhere.
* write - bool whether to write or delete, true is write, false is delete
* folder - bool is path a folder or a file.
* success status

### Push

Arguments:

* path of file
* file

Client indicates that the server's version of the named file is out of date and is providing a new one.

Returns:

* success status

### Delete

Arguments:

* path of file

Client indicates that the server's version of the named file has been deleted.

Returns:

* success status

## Future

* Compression
* Differentials
* Making unstable internet connection less of an issue
* Server should react to multiple connections.
* Write while downloading.
