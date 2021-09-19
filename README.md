
# Parsing bigip_gtm.conf

in certain automation scenarios, when you have several thousands of GTM server objects (Servers, WideIPs, Pools) it might take longer than expected to get all the objects through REST API. 
This repo provides an alternative way to get similar details but through the bigip_gtm.conf file. 


## Option A - Downloading bigip_gtm.conf snd parsing it locally

In this option we are using the server used for the automation pipeline to connect via scp (Secure Copy Protocol) that will connect to F5 and download the BigIP GTM configuration file. Once the file is downloaded, it will run a python script against it so that extracts the right information. 

In the example below we are using a PHP server for the HTTP endpoint and Python for downloading the configuration file from BigIP and parsing the data locally. 

### How it works. 

The client (user or app) will make a request to the PHP endpoint specifying to provide the records either for servers/pools/wideips `https://<IP>/endpoint.php?retrieve=pool`. PHP script (endpoint.php) will get the variable `retrieve` that can have 3 values.


| retrieve values    |
|--------------------|
| server	       |
| pool	         |
| wideip      |

The PHP script will call the Python script (get_file.py) that will in turn connect to bigip, download the `bigip_gtm.conf` file with scp and save it as `config.conf`
Once the file is stored, Python will parse the file and provide the Servers/Pools/WideIPs results in json format. 

### Benefits.
+ With this option there is no additional process or script that is deployed in BIGIP that will consume CPU resources. 
+ Even if the Python script fails to parse there is little concern as it takes place outside BIGIP.
- It will take an additional 1-2 seconds to download the file from BIGIP.


You can find both scripts <a href="https://github.com/skenderidis/gtm-parsing/tree/main/Option%20A"> here </a>


## Option B - Parsing bigip_gtm.conf on GTM and getting results

In this option we are using the server used for the automation pipeline to connect via scp (Secure Copy Protocol) that will connect to F5 and download the BigIP GTM configuration file. Once the file is downloaded, it will run a python script against it so that extracts the right information. 

In the example below we are using a PHP server for the HTTP endpoint and Python for downloading the configuration file from BigIP and parsing the data locally. 