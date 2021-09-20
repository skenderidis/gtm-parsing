
# Testing

It is critical to test the behavior of your infrastructure on a lab environment.

The following are 2 Python scripts that can help you evaluate the performance impact of the 2 options.



1. Script `script-dns.py` can perform hundreds of DNS queries per second so that you can put your GTM under some realistic load (DO NOT EXECUTE ON YOU PRODUCTION ENVIRONMENT)



```shell
import socket
from datetime import datetime
import time

limit = 5   ### "How many DNS requets you want to execute? (for example 10,000): ")
dns_name = "www.test.local"  #### "What is the hostname you want to resolve? (for example www.test.local): ")
sleep_time = 0.005 ##### Sleep between DNS requests. 0.005 is 5 milliseconds while 1 is 1 second.
start_time = datetime.now()
addr1="Failed"

x=0
y=0
while True:
    x=x+1
	time.sleep (sleep_time)
    try:
        addr1 = socket.gethostbyname(dns_name)
#        print(addr1)

    except Exception, exc:
#        print("error while processing item:")
        y=y+1
    if x>=limit:
        break;


end_time = datetime.now()

print("Attempted DNS requests:" + str(x))
print("Failed DNS requests:" + str(y))
print('Duration: {}'.format(end_time - start_time))
print(addr1)

```


2. Script `script-bash.py` can execute mulitple queries to the bash script per minut so that you can put your GTM under some realistic load (DO NOT EXECUTE ON YOU PRODUCTION ENVIRONMENT). The default for the script is 1 per minute, but can be changed by modifying the sleep_time variable.

```shell
import http.client
import ssl
import json
import time
from datetime import datetime

start_time = datetime.now()
sleep_time = 60              ##### Sleep between DNS requests. 0.005 is 5 milliseconds while 60 is 60 seconds.

x=0
while True:
    if x>=100:
        break;
    
    x=x+1
    
    conn = http.client.HTTPSConnection("192.168.5.91",context = ssl._create_unverified_context())
    payload = json.dumps({
    "command": "run",
    "utilCmdArgs": "-c /config/server.sh"
    })
    headers = {
    'Authorization': 'Basic YWRtaW46S29zdGFzMTIz',
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/mgmt/tm/util/bash", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    
    time.sleep (sleep_time)
 
print("Successfull queries requests:" + str(x))
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

```