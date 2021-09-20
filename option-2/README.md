
# Option B - Parsing bigip_gtm.conf on GTM and getting results

## Pre-requisites

* PHP server (Optional)

## How to install it

#### Step1
Upload the three Bash and Python scripts to one GTM on conf

#### Step2
Modify the Python script `get_file.py` to include  `IP address, Username and Password` of the BIGIP device you want to connect to

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


