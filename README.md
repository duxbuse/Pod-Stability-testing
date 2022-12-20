Stability testing

Are there any existing programs that can be leveraged?
	- Chaos mesh
	- Chaos monkey
	- litmus

Things we want to test:
	- Pod scaling time
	- PDBs
	- Pod cold start
	- pod shutdown time
	- SIGINT SIGTERM

Reporting
	- success/failure
	- report of metrics

CLI tool that is pointed at a deployment
 Initial script that create kuberenetes object, retrieve the deployment definition, do other things
	— potentially piggyback on pytest, can customise reports
Each test defined as it’s own script
Json object returned for reporting
Generates report


## Usage

The whole things is designed as a pytest suite.
There is also the appropriate vscode config set up.
But otherwise running `pytest --deployment abc --namespace default` will run the suite targeting the relevant deployment and namespace.