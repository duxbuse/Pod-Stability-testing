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

— main.py
	— /tests
		— test1.py (test(k, d))