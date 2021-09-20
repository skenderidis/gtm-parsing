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