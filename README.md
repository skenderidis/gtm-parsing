
# Parsing bigip_gtm.conf

In certain automation scenarios, when you have several thousands of GTM server objects (Servers, WideIPs, Pools) it might take longer than expected to get all the objects through REST API. 
This repo provides an alternative way to get similar details by parsing the bigip_gtm.conf file. 


## Option A - Downloading bigip_gtm.conf and parsing it locally

In this option we are using the server used for the automation pipeline to connect via scp (Secure Copy Protocol) that will connect to F5 and download the BigIP GTM configuration file. Once the file is downloaded, it will run a Python script against it and extract the required information. 

In the example below we are using a PHP server for the HTTP endpoint and Python for downloading the configuration file from BigIP and parsing the data locally. 

### How it works

The client (user or app) will make a request to the PHP endpoint specifying to provide the records either for servers/pools/wideips `https://php-ip-address/endpoint.php?retrieve=pool`. PHP script (endpoint.php) will get the variable `retrieve` that can have 3 values (see below).


| retrieve values    |
|--------------------|
| server	       |
| pool	         |
| wideip      |

The PHP script will call the Python script (get_file.py) that will in turn connect to bigip, download the `bigip_gtm.conf` file (with the use of scp), and save it as `config.conf`
Once the file is stored, Python will parse the file and provide the Servers/Pools/WideIPs results in json format. 

### Benefits
(+) With this option there is no additional process or script that is deployed in BIGIP that will consume CPU resources.

(+) Even if the Python script fails to parse there is little concern as it takes place outside BIGIP.

(-) It will take an additional 1-2 seconds to download the file from BIGIP.


You can find both scripts <a href="https://github.com/skenderidis/gtm-parsing/tree/main/Option%20A"> here </a>


## Option B - Parsing bigip_gtm.conf on GTM and getting results

In this option we are have 3 Python scripts that parse the BigIP GTM configuration file and extract the required information. 

### How it works

The client (user or app) will make a request to the endpoint `https://gtm-ip-address/mgmt/tm/util/bash` and will provide 3 different post values depending whether we need servers/pools/wideips.

| POST DATA    |
|--------------------|
| {"command": "run", "utilCmdArgs": "-c /config/servers.sh"}	       |
| {"command": "run", "utilCmdArgs": "-c /config/pools.sh"}	       |
| {"command": "run", "utilCmdArgs": "-c /config/wideips.sh"}	       |

The Bash scripts will copy the existing `bigip_gtm.conf` file to a temporary file called `temp.conf` and then execute the Python script to parse the `temp.conf` files and provide the json output. 

Bash script `servers.sh` is shown below

```shell
#!/bin/bash
cp /config/bigip_gtm.conf /config/temp.conf
python /config/server.py

```
All scripts for this option can be found <a href="https://github.com/skenderidis/gtm-parsing/tree/main/Option%20B"> here </a>

### Benefits
(+) Faster than Option A, as it doesn't require downloading the file 

(-) Since the Python script is executed on the BIGIP it consumes resources from the system. So depending on the # of calls this needs to be considered.

(-) It is important to validate that the Python script will not go into a loop (after a change) as it could have an impact on the control plane CPU of the BIGP  


## General Recommendations
* It is highly recommended to have a "shadow" GTM that will be used only for REST API purposes. 
* Before changes please perform a test on a lab environment.
* Validate the Python scripts as per your requirements. The provided scripts are for testing purposes.
