# Fig

Folder sharing tool.



## Comms

Client sends out packages and gets replies. Server never initiates. Here is a list of packages the client can send and the matching server responses with some explanations.

### Fetch

No arguments

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
	"times": {
		"foo": 1544619124,
		"foo.png": 1544619124,
		"bar": 1544619124,
		"bur": 1544619124,
		"bur.py": 1544619124,
		"bar": 1544619124,
	}
}
```

### Pull

Arguments:

* path of file

Client indicates that their version of the named file is out of date and is requesting it from the server.

Returns:

* file
* success status

### Push

Arguments:

* path of file
* file

Client indicates that the server's version of the named file is out of date and is providing a new one.

Returns:

* success status

## Future

Compression, differentials
