
# Option A - Downloading bigip_gtm.conf and parsing it locally

## Pre-requisites

* PHP server
* Python
* Python modules requests and scp

## How to install it

#### Step1
Put both files ` endpoint.php, get_file.py `  on the same directory on a PHP server. 

#### Step2
Modify the Python script `get_file.py` with the correct  `IP address, Username and Password` of the BIGIP device you want to connect to

```shell
import re
import json
import paramiko
from scp import SCPClient
import sys

... 
...
...
...

######   BIGIP variables #########
bigip_ip_address="192.168.5.91"   ####  <=========   Update these values with the IP Address 
username="root"                   ####  <=========   Update these values with the "Username" 
password="Test123"                ####  <=========   Update these values with the "Password" 
```

#### Step3
Connect to the endpoints:
* For Servers: `https://php-ip-address/endpoint.php?retrieve=server`
* For WideIPs: `https://php-ip-address/endpoint.php?retrieve=wideip`
* For Pools: `https://php-ip-address/endpoint.php?retrieve=pool`


