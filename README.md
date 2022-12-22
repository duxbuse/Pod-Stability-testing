# Pod Stability testing

## Goals

Things we want to test:
	- Pod scaling time
	- PDBs
	- Pod cold start
	- pod shutdown time
	- SIGINT SIGTERM


## Usage

The whole things is designed as a pytest suite.
There is also the appropriate vscode config set up.
But otherwise running `pytest --deployment abc --namespace default` will run the suite targeting the relevant deployment and namespace.



